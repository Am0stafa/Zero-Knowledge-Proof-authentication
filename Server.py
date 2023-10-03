import socket
import threading
import json
import os
import numpy

data_file = 'users.json'

def load_users():
  if os.path.exists(data_file):
    with open(data_file, 'r') as f:
      try:
        return json.load(f)
      except json.JSONDecodeError:
        print("The users file is empty")
        return {}
  print("The users file does not exist")
  return {}


def save_users(users):
    with open(data_file, 'w') as f:
        json.dump(users, f)

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    route, _, data = request.partition(' ')
    username, _, password = data.partition(' ')
    
    users = load_users()

    if route == '/signup':
        if username in users:
            client_socket.send("Username already taken".encode())
        else:
            users[username] = password
            save_users(users)
            client_socket.send("Signup successful".encode())
    elif route == '/login':
        if users.get(username) == password:
            client_socket.send("Login successful".encode())
        else:
            client_socket.send("Login failed".encode())
    else:
        client_socket.send("Invalid route".encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
