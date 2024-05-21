import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import hashlib
import random
import socket
import json
import threading
import os
import libnum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Global variables for client
n = 997
g = 3
salt = "S0m3_S4lt"
data_file = 'users.json'
file_lock = threading.Lock()

# Server functionality
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
        if username not in users:
            client_socket.send("Invalid username".encode())
        else:
            providedT = int(password)
            c = random.randint(1, 997)
            client_socket.send(str(c).encode())

            response_data = client_socket.recv(1024).decode()
            if 'r value for' in response_data:
                _, _, _, _, nameForR, r_value = response_data.split(' ')
                r = int(r_value)
                y = int(users[username])

                if r < 0:
                    Result = (libnum.invmod(pow(g, -r, n), n) * pow(y, c, n)) % n
                else:
                    Result = (pow(g, r, n) * pow(y, c, n)) % n

                if Result == providedT:
                    client_socket.send("Login successful".encode())
                else:
                    client_socket.send("Login failed".encode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

class ZKPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZKP Authentication System")
        self.root.geometry("1200x800")
        self.create_main_page()

    def create_main_page(self):
        self.clear_window()

        title_label = tk.Label(self.root, text="Zero-Knowledge Proof Authentication", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Explanation Panels
        explanation_frame = tk.Frame(self.root)
        explanation_frame.pack(pady=10)

        reg_explanation = tk.Label(explanation_frame, text="Registration: Your password will be hashed and a public key generated. This public key will be stored on the server.", wraplength=450, justify="left")
        reg_explanation.grid(row=0, column=0, padx=10)

        login_explanation = tk.Label(explanation_frame, text="Login: A random value `v` will be generated and `t` will be computed. The server will send a challenge `c`, and you will respond with `r = v - c * x`. The server will verify your proof without knowing your password.", wraplength=450, justify="left")
        login_explanation.grid(row=0, column=1, padx=10)

        # User Registration
        reg_frame = tk.LabelFrame(self.root, text="User Registration", padx=10, pady=10)
        reg_frame.pack(pady=10)

        tk.Label(reg_frame, text="Username:").grid(row=0, column=0, sticky='w')
        self.reg_username_entry = tk.Entry(reg_frame, width=30)
        self.reg_username_entry.grid(row=0, column=1)

        tk.Label(reg_frame, text="Password:").grid(row=1, column=0, sticky='w')
        self.reg_password_entry = tk.Entry(reg_frame, width=30, show="*")
        self.reg_password_entry.grid(row=1, column=1)

        self.reg_progress = ttk.Progressbar(reg_frame, orient="horizontal", length=200, mode="determinate")
        self.reg_progress.grid(row=2, columnspan=2, pady=5)

        self.reg_button = tk.Button(reg_frame, text="Sign Up", command=self.signup)
        self.reg_button.grid(row=3, columnspan=2, pady=5)

        # User Login
        login_frame = tk.LabelFrame(self.root, text="User Login", padx=10, pady=10)
        login_frame.pack(pady=10)

        tk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky='w')
        self.login_username_entry = tk.Entry(login_frame, width=30)
        self.login_username_entry.grid(row=0, column=1)

        tk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky='w')
        self.login_password_entry = tk.Entry(login_frame, width=30, show="*")
        self.login_password_entry.grid(row=1, column=1)

        self.login_progress = ttk.Progressbar(login_frame, orient="horizontal", length=200, mode="determinate")
        self.login_progress.grid(row=2, columnspan=2, pady=5)

        self.login_button = tk.Button(login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, columnspan=2, pady=5)

        # Server Status
        server_frame = tk.LabelFrame(self.root, text="Server Status", padx=10, pady=10)
        server_frame.pack(pady=10)

        self.server_status_label = tk.Label(server_frame, text="Server is stopped")
        self.server_status_label.grid(row=0, column=0, padx=10)

        self.server_button = tk.Button(server_frame, text="Start Server", command=self.start_server_thread)
        self.server_button.grid(row=0, column=1, padx=10)

        # Logs and Visualization
        logs_frame = tk.LabelFrame(self.root, text="Logs and Visualization", padx=10, pady=10)
        logs_frame.pack(pady=10, fill='both', expand=True)

        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=15)
        self.logs_text.pack(pady=5, fill='both', expand=True)

        clear_logs_button = tk.Button(logs_frame, text="Clear Logs", command=self.clear_logs)
        clear_logs_button.pack()

        # Canvas for Graphs
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=logs_frame)
        self.canvas.get_tk_widget().pack(pady=10, fill='both', expand=True)

        # Code and Mathematical Formulas Display
        code_frame = tk.LabelFrame(self.root, text="Code and Mathematical Formulas", padx=10, pady=10)
        code_frame.pack(pady=10, fill='both', expand=True)

        self.code_text = scrolledtext.ScrolledText(code_frame, height=10)
        self.code_text.pack(pady=5, fill='both', expand=True)

        # Real-Time Cryptographic Calculations
        calc_frame = tk.LabelFrame(self.root, text="Real-Time Cryptographic Calculations", padx=10, pady=10)
        calc_frame.pack(pady=10, fill='both', expand=True)

        tk.Label(calc_frame, text="Enter value for v:").grid(row=0, column=0, sticky='w')
        self.calc_v_entry = tk.Entry(calc_frame, width=20)
        self.calc_v_entry.grid(row=0, column=1)

        calc_button = tk.Button(calc_frame, text="Calculate", command=self.calculate_cryptographic_steps)
        calc_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.calc_results_text = scrolledtext.ScrolledText(calc_frame, height=10)
        self.calc_results_text.grid(row=2, column=0, columnspan=2, pady=5, sticky='nsew')

        # Initially disable registration and login until server is started
        self.reg_username_entry.config(state=tk.DISABLED)
        self.reg_password_entry.config(state=tk.DISABLED)
        self.reg_button.config(state=tk.DISABLED)
        self.login_username_entry.config(state=tk.DISABLED)
        self.login_password_entry.config(state=tk.DISABLED)
        self.login_button.config(state=tk.DISABLED)

    def start_server_thread(self):
        self.server_thread = threading.Thread(target=start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.server_status_label.config(text="Server is running")
        self.server_button.config(state=tk.DISABLED)
        self.log("Server started", "green")

        # Enable registration and login once server is started
        self.reg_username_entry.config(state=tk.NORMAL)
        self.reg_password_entry.config(state=tk.NORMAL)
        self.reg_button.config(state=tk.NORMAL)
        self.login_username_entry.config(state=tk.NORMAL)
        self.login_password_entry.config(state=tk.NORMAL)
        self.login_button.config(state=tk.NORMAL)

    def signup(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        self.reg_progress['value'] = 0

        if ' ' in username:
            self.log("Username cannot contain spaces", "red")
            return

        users = load_users()

        if username in users:
            self.log("Username already taken", "red")
        else:
            self.reg_progress['value'] = 20
            hashed_password = hashlib.md5((password + salt).encode()).hexdigest()
            self.reg_progress['value'] = 40
            x = int(hashed_password, 16) % n
            self.reg_progress['value'] = 60
            y = pow(g, x, n)
            self.reg_progress['value'] = 80
            users[username] = y
            save_users(users)
            self.reg_progress['value'] = 100
            self.log("User Registration: Hashing password...", "blue")
            self.log("User Registration: Generating public key...", "blue")
            self.visualize(f"Hashed Password: {hashed_password}\nPublic Key (y): {y}", "blue")
            self.log("User Registration: Sign-up successful.", "green")
            messagebox.showinfo("Success", "Sign-up successful!")

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        self.login_progress['value'] = 0

        users = load_users()

        if username not in users:
            self.log("Invalid username", "red")
        else:
            self.login_progress['value'] = 20
            v = random.randint(1, n)
            t = pow(g, v, n)
            self.login_progress['value'] = 40
            self.log("User Login: Generating random value `v`...", "blue")
            self.log("User Login: Computing `t = g^v % n`...", "blue")
            self.visualize(f"Generated v: {v}\nComputed t: {t}", "blue")

            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('127.0.0.1', 9999))
            except ConnectionRefusedError:
                self.log("Server connection refused. Ensure the server is running.", "red")
                return

            request = f'/login {username} {t}'
            client_socket.send(request.encode())

            c = int(client_socket.recv(4096).decode())
            self.login_progress['value'] = 60
            self.log("User Login: Server challenge `c` received...", "blue")
            self.visualize(f"Server challenge c: {c}", "blue")

            hashed_password = hashlib.md5((password + salt).encode()).hexdigest()
            x = int(hashed_password, 16) % n
            r = v - c * x
            self.login_progress['value'] = 80
            self.log("User Login: Computing `r = v - c * x`...", "blue")
            self.visualize(f"Hashed Password: {hashed_password}\nComputed r: {r}", "blue")

            request_r = f'/login r value for {username} {r}'
            client_socket.send(request_r.encode())

            response = client_socket.recv(4096).decode()
            self.login_progress['value'] = 100
            self.log("User Login: Verifying proof...", "blue")

            if "successful" in response:
                self.log("User Login: Login successful.", "green")
                messagebox.showinfo("Success", "Login successful!")
            else:
                self.log("User Login: Login failed.", "red")
                messagebox.showerror("Error", "Login failed.")

            client_socket.close()

    def calculate_cryptographic_steps(self):
        v = self.calc_v_entry.get()
        if not v.isdigit():
            messagebox.showerror("Error", "Please enter a valid number for v.")
            return

        v = int(v)
        t = pow(g, v, n)
        self.calc_results_text.delete(1.0, tk.END)
        self.calc_results_text.insert(tk.END, f"Generated v: {v}\nComputed t: {t}\n")

        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, "Code Snippet:\n")
        self.code_text.insert(tk.END, f"v = {v}\nt = pow(g, v, n)\n")
        self.code_text.insert(tk.END, "Mathematical Formula:\n")
        self.code_text.insert(tk.END, f"t = g^v % n\n")

    def clear_logs(self):
        self.logs_text.delete(1.0, tk.END)
        self.ax.clear()
        self.canvas.draw()

    def log(self, message, color):
        self.logs_text.insert(tk.END, f"{message}\n")
        self.logs_text.tag_add("log", "end-2l", "end-1l")
        self.logs_text.tag_config("log", foreground=color)

    def visualize(self, message, color):
        self.logs_text.insert(tk.END, f"{message}\n")
        self.logs_text.tag_add("visualize", "end-2l", "end-1l")
        self.logs_text.tag_config("visualize", foreground=color, font=("Helvetica", 10, "bold"))
        self.plot_graph(message)

    def plot_graph(self, message):
        self.ax.clear()
        self.ax.text(0.5, 0.5, message, transform=self.ax.transAxes, fontsize=12, verticalalignment='center', horizontalalignment='center')
        self.canvas.draw()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZKPApp(root)
    root.mainloop()
