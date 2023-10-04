import socket
import random
import hashlib

def login(username,password):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('127.0.0.1', 9999))
  n = 997
  g = 3
  v = random.randint(1,n)
  t = pow(g,v,n)
  request = f'/login {username} {t}'
  client.send(request.encode())
  response = client.recv(4096)
  c = int(response.decode()) # the server send the c which is the challenge
  x = int(hashlib.md5(password).hexdigest()[:8], 16) % n
  r = (v - c * x)
  # send it to the server
  client.send(str(f'/login r value for {username} is {r}').encode())

# Usage:
login('john_doe', 'password123')
