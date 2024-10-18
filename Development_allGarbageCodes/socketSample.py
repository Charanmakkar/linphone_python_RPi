import socket

def send_post_request(host, port, path, payload):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    
    # Construct the HTTP POST request
    post_request = f"POST {path} HTTP/1.1\r\n"
    post_request += f"Host: {host}\r\n"
    post_request += "Content-Type: application/Charan\r\n"
    post_request += f"Content-Length: {len(payload)}\r\n"
    post_request += "Connection: close\r\n\r\n"
    post_request += payload
    
    # Send the request
    client_socket.sendall(post_request.encode())
    
    # Receive the response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    # Close the socket
    client_socket.close()
    
    # Print the response
    print(response.decode())

# Usage example
host = '192.168.1.200'   # Server's hostname or IP
port = 50050              # HTTP port (usually 80)
path = '/path'         # Server's resource path
payload = 'key1=value1&key2=value2'  # Example payload as a URL-encoded string

send_post_request(host, port, path, payload)
