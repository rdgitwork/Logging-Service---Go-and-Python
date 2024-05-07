import socket
import threading
import yaml
from datetime import datetime
from collections import defaultdict
import time

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def log_message(client_info, message_level, message, file_path, log_format):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = log_format.format(timestamp=timestamp, client_info=client_info, message_level=message_level, message=message)
    with open(file_path, 'a') as file:
        file.write(formatted_message + '\n')

message_counts = defaultdict(lambda: [0, time.time()])

def control_limit(address, message_counts, limit=30, window=60):
    
    current_time = time.time()
    msgs, last_time = message_counts.get(address, (0, current_time))

    # Reset count for a new window
    if current_time - last_time > window:
        message_counts[address] = (1, current_time)
        return False
    
    if msgs >= limit:
        return True  # Rate limit exceeded
    else:
        # Increment the message count for the current window
        message_counts[address] = (msgs + 1, last_time)
        return False
    
    


active_usernames = set()

def client_server_part(connection, address, config):
    global message_counts, active_usernames  # Ensure access to the global variables

    try:
        username = connection.recv(1024).decode('utf-8').strip()
        client_info = f"{username}({address[0]}:{address[1]})"

        # Check if username is already active
        if username in active_usernames:
            print(f"Refusing connection from {client_info}: Username already in use.")
            connection.sendall("Connection refused: Username already in use.\n".encode('utf-8'))
            connection.close()
            return
        else:
            active_usernames.add(username)
            print(f"Connection from {client_info} has been established.")
            log_message(client_info, "LOG", "Client connected", config['log']['file_path'], config['log']['format'])

        while True:
            message = connection.recv(1024).decode('utf-8').strip()
            if not message:
                break  # Client disconnected
            
            print(f"Received message from {client_info}: {message}")

            if control_limit(address, message_counts):
                print(f"Rate limit exceeded for {client_info}. Disconnecting.")
                log_message(client_info, "WARNING", "Disconnected due to rate limit exceedance", config['log']['file_path'], config['log']['format'])
                break  # Exit the loop to disconnect the client

            # Process the received message
            message_level, message_content = "INFO", message  # Default level
            if message.startswith("CUSTOM:"):
                _, message_content = message.split("CUSTOM:", 1)
                message_level = "CUSTOM"
            log_message(client_info, message_level, message_content, config['log']['file_path'], config['log']['format'])

    except Exception as e:
        print(f"Error handling message from {client_info}: {e}")
    finally:
        active_usernames.discard(username)  # Remove the username from active set on disconnection
        log_message(client_info, "LOG", "Client disconnected", config['log']['file_path'], config['log']['format'])
        connection.close()
        print(f"Connection from {client_info} has been closed.")



def initiate_start(config):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config['server']['host'], config['server']['port']))
    server_socket.listen(5)
    print(f"Listening on {config['server']['host']}:{config['server']['port']} for connections...")
    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=client_server_part, args=(client_socket, address, config)).start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    config = load_config()
    initiate_start(config)
