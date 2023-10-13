import socket
import random
import hashlib
from colorama import init,Fore

init()
n = 997
g = 3
salt = "S0m3_S4lt"

def login(username, password):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('127.0.0.1', 9999))
  v = random.randint(1, n)
  print(Fore.GREEN + f"The user {username} generated a random value v with the value of {v}" + Fore.RESET)
  t = pow(g, v, n)
  print(Fore.GREEN + f"The user {username} generated a random value t with the value of {t}" + Fore.RESET)
  request = f'/login {username} {t}'
  client.send(request.encode())
  c = int(client.recv(4096).decode())
  print(Fore.GREEN + f"Server generated a random value c with the value of {c} to this user {username}" + Fore.RESET)
  hashed_password = hashlib.md5((password + salt).encode()).hexdigest()
  x = int(hashed_password, 16) % n
  print(Fore.GREEN + f"The user {username} hashed the password with mod {n} which computed to {x}" + Fore.RESET)
  r = v - c * x
  print(Fore.GREEN + f"The user {username} computed the value of r as {r}" + Fore.RESET)
  request_r = f'/login r value for {username} {r}'
  client.send(request_r.encode())
  response = client.recv(4096)
  print(response.decode())

login('john2', 'password123')
