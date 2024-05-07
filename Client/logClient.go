package main

import (
    "bufio"
    "flag"
    "fmt"
    "net"
    "os"
    "strings"
)

func main() {
    host := flag.String("host", "localhost", "Server IP address")
    port := flag.String("port", "8080", "Server port")
    automatedTest := flag.Bool("test", false, "Run automated tests")
	abuseTest := flag.Bool("abuse", false, "Enable abuse testing")


    flag.Parse()

    serverAddress := *host + ":" + *port

    
    if *automatedTest {
        runAutomatedTests(serverAddress)
        return
    }

	 if *abuseTest {
        runAbuseTests(serverAddress)
        return
    }
	
    connectAndSendLogs(serverAddress)
}

func runAutomatedTests(serverAddress string) {
    
    testMessages := []string{"INFO,This is an info message", "ERROR,This is an error message", "DEBUG,This is a debug message"}
    for _, message := range testMessages {
        sendMessage(serverAddress, message, 1) // Send each message once
    }
    fmt.Println("Automated tests completed.")
}

func sendMessage(serverAddress, message string, times int) {
    conn, err := net.Dial("tcp", serverAddress)
    if err != nil {
        fmt.Println("Error connecting:", err)
        return
    }
    defer conn.Close()

    for i := 0; i < times; i++ {
        _, err := conn.Write([]byte(message + "\n"))
        if err != nil {
            fmt.Println("Server is closed or connection lost:", err)
            return
        }
    }
    fmt.Printf("Message '%s' sent %d times.\n", message, times)
}


func connectAndSendLogs(serverAddress string) {
    conn, err := net.Dial("tcp", serverAddress)
    if err != nil {
        fmt.Println("Error connecting:", err.Error())
        return
    }
	defer conn.Close()

    defer func() {
        _, _ = conn.Write([]byte("DISCONNECT\n")) // Send disconnection message before closing
        conn.Close()
        fmt.Println("Disconnected from server.")
    }()

    
    fmt.Print("Enter your username: ")
    reader := bufio.NewReader(os.Stdin)
    username, _ := reader.ReadString('\n')
    username = strings.TrimSpace(username) // Trim newline character
    _, err = conn.Write([]byte(username + "\n"))
    if err != nil {
        fmt.Println("Error sending username:", err.Error())
        return
    }

    fmt.Println("Connected to server. Enter 'messagelevel,message' to send logs ('quit' to stop):")
    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan() {
        text := scanner.Text()
        if strings.ToLower(text) == "quit" {
            break
        }
        _, err = conn.Write([]byte(text + "\n"))
        if err != nil {
            fmt.Println("Server is closed or connection lost:", err)
            break
        }
    }
    fmt.Println("Disconnected from server or server closed.")
}

func runAbuseTests(serverAddress string) {
    conn, err := net.Dial("tcp", serverAddress)
    if err != nil {
        fmt.Println("Error connecting for abuse tests:", err)
        return
    }
    defer conn.Close()

    
    for i := 0; i < 100; i++ {
        message := fmt.Sprintf("ABUSE,This is abuse message #%d", i)
        _, err := conn.Write([]byte(message + "\n"))
        if err != nil {
            fmt.Println("Failed to send abuse message:", err)
            return
        }
    }
    fmt.Println("Abuse testing completed. Sent 100 messages rapidly.")
}
