import socket
import os

HOST, PORT = 'localhost', 8080
BASE_DIR = './www'

mime_types = {
    ".html": "text/html",
    ".css": "text/css",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".js": "application/javascript",
}

def handle_request(client_connection):
    request = client_connection.recv(1024).decode()
    print(request.splitlines()[0])

    try:
        # Parsing la richiesta GET
        first_line = request.splitlines()[0]
        file_requested = first_line.split(' ')[1]

        if file_requested == '/':
            file_requested = '/index.html'

        filepath = BASE_DIR + file_requested

        if not os.path.isfile(filepath):
            raise FileNotFoundError

        with open(filepath, 'rb') as file:
            content = file.read()

        ext = os.path.splitext(filepath)[1]
        mime_type = mime_types.get(ext, "application/octet-stream")

        header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n"
    except FileNotFoundError:
        header = "HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n"
        content = b"<h1>404 Page Not Found</h1>"

    response = header.encode() + content
    client_connection.sendall(response)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server running at http://{HOST}:{PORT}/")

        while True:
            client_connection, _ = server_socket.accept()
            handle_request(client_connection)
            client_connection.close()

if __name__ == '__main__':
    run_server()
