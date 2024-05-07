# Logging Service - Go Client and Python Server

This project implements a logging service using Go for the client-side and Python for the server-side. It allows communication between devices over a VPN connection, enabling centralized logging from various devices.

## Features
- **Go Client**: Logs messages from client devices.
- **Python Server**: Receives and stores logged messages.
- **VPN Access**: Secure communication between devices over VPN.

## Deployment

### Server Deployment (Python)

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the `server` directory: `cd server`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python server.py`

### Client Deployment (Go)

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the `client` directory: `cd client`
3. Build the Go client: `go build -o client`
4. Run the client: `./client`

Make sure to configure the VPN connection between the client and server devices before deployment.

## Screenshots

[Include screenshots of the running application here]

### Server Interface

![Server Interface](server_interface.png)

### Client Interface

![Client Interface](client_interface.png)



---

Feel free to contribute to the project or provide feedback by opening issues or pull requests. Happy logging!
