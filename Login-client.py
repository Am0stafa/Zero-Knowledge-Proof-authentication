import socket
import random
import hashlib

n = 997
g = 3
salt = "S0m3_S4lt"

def login(username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    v = random.randint(1, n)
    t = pow(g, v, n)
    request = f'/login {username} {t}'
    client.send(request.encode())
    c = int(client.recv(4096).decode())
    hashed_password = hashlib.md5((password + salt).encode()).hexdigest()
    x = int(hashed_password, 16) % n
    r = v - c * x
    request_r = f'/login r value for {username} {r}'
    client.send(request_r.encode())
    response = client.recv(4096)
    print(response.decode())

login('john2', 'password123')
