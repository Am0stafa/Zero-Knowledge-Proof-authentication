import socket

def login(username, password):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('127.0.0.1', 9999))
  request = f'/login {username} {password}'
  client.send(request.encode())
  response = client.recv(4096)
  print(response.decode())

# Usage:
login('john_doe', 'password123')
