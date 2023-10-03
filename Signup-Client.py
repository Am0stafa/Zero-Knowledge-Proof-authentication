# It hashes the password to generate a "public key" public key based on the password and sends this along with the username to the server

import socket
import hashlib

def signup(username, password):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('127.0.0.1', 9999))
  
  # Generate public key
  public_key = hashlib.sha256(password.encode()).hexdigest()
  request = f'/signup {username} {public_key}'
  client.send(request.encode())
  response = client.recv(4096)
  print(response.decode())

# Usage:
signup('john_doe', 'password123')
