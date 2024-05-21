import socket
import threading
import json
import os
import random
import libnum
from colorama import init, Fore

init()
data_file = 'users.json'
g = 3
n = 997
salt = "S0m3_S4lt"
file_lock = threading.Lock()

def load_users():
    with file_lock:
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

def save_users(users):
    with file_lock:
        with open(data_file, 'w') as f:
            json.dump(users, f)

def handle_client(client_socket, addr):
    print(Fore.GREEN + f"Connection from {addr}" + Fore.RESET)
    request = client_socket.recv(1024).decode()
    print(Fore.GREEN + f"Received request: {request}" + Fore.RESET)
    route, _, data = request.partition(' ')
    username, _, password = data.partition(' ')

    users = load_users()

    if route == '/signup':
        print(Fore.GREEN + f"User {username} of address {addr} is trying to signup" + Fore.RESET)
        if username in users:
            client_socket.send("Username already taken".encode())
            print(Fore.RED + f"Username {username} already taken" + Fore.RESET)
        else:
            users[username] = password
            save_users(users)
            print(Fore.GREEN + f"User {username} of address {addr} signed up successfully" + Fore.RESET)
            client_socket.send("Signup successful".encode())

    elif route == '/login':
        if username not in users:
            client_socket.send("Invalid username".encode())
            print(Fore.RED + f"Invalid username {username} for address {addr}" + Fore.RESET)
        else:
            providedT = int(password)
            print(Fore.GREEN + f"User {username} of address {addr} sent the value of t as {providedT}" + Fore.RESET)
            c = random.randint(1, 997)
            print(Fore.GREEN + f"Server generated a random value c with the value of {c} for this user {username} with this address {addr}" + Fore.RESET)
            client_socket.send(str(c).encode())

            response_data = client_socket.recv(1024).decode()

            if 'r value for' in response_data:
                _, _, _, _, nameForR, r_value = response_data.split(' ')
                r = int(r_value)
                print(Fore.GREEN + f"User {nameForR} of address {addr} sent the value of r as {r}" + Fore.RESET)
                y = int(users[username])

                if r < 0:
                    Result = (libnum.invmod(pow(g, -r, n), n) * pow(y, c, n)) % n
                else:
                    Result = (pow(g, r, n) * pow(y, c, n)) % n

                if Result == providedT:
                    client_socket.send("Login successful".encode())
                else:
                    client_socket.send("Login failed".encode())
            else:
                client_socket.send("Invalid request".encode())
    else:
        client_socket.send("Invalid route".encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        print("Waiting for a connection...")
        try:
            client_socket, addr = server.accept()
        except Exception as e:
            print("An error occurred while accepting a connection")
            print(e)
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
