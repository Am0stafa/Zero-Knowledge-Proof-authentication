import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

# List to store registered usernames for the sake of this example
registered_usernames = {}
users_credentials = {"admin": "password"}

# Sample functions for sign up and login
def signup(username, password):
    if username in registered_usernames:
        return False
    registered_usernames[username] = password
    users_credentials[username] = password
    return True

def login(username, password):
    if username in users_credentials and users_credentials[username] == password:
        return True
    return False

def fade_frame(frame, direction=1):
    alpha = frame.winfo_toplevel().attributes('-alpha')
    if direction == 1:
        if alpha < 1:
            alpha += 0.1
            frame.winfo_toplevel().attributes('-alpha', alpha)
            frame.after(30, lambda: fade_frame(frame, direction=1))
    else:
        if alpha > 0:
            alpha -= 0.1
            frame.winfo_toplevel().attributes('-alpha', alpha)
            frame.after(30, lambda: fade_frame(frame, direction=0))
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.winfo_toplevel().attributes('-alpha', 1)

# GUI functions
def show_signup():
    for widget in app.winfo_children():
        widget.destroy()
    
    signup_title_label = tk.Label(app, text="Sign Up", font=("Arial", 24))
    signup_title_label.pack(pady=10)

    signup_username_label = tk.Label(app, text="Username")
    signup_username_label.pack(pady=5)
    signup_username_entry = ctk.CTkEntry(app)
    signup_username_entry.pack(pady=5)

    signup_password_label = tk.Label(app, text="Password")
    signup_password_label.pack(pady=5)
    signup_password_entry = ctk.CTkEntry(app, show="*")
    signup_password_entry.pack(pady=5)

    def process_signup():
        username = signup_username_entry.get()
        password = signup_password_entry.get()
        if signup(username, password):
            show_main()
        else:
            messagebox.showerror("Error", "Username is already taken!")

    signup_process_btn = ctk.CTkButton(app, text="Sign Up", command=process_signup, bg_color="#2E7BFF")
    signup_process_btn.pack(pady=10)

    back_btn = ctk.CTkButton(app, text="Back", command=show_main, bg_color="#D3D3D3")
    back_btn.pack(pady=10)

def show_login():
    for widget in app.winfo_children():
        widget.destroy()
    
    login_title_label = tk.Label(app, text="Login", font=("Arial", 24))
    login_title_label.pack(pady=10)

    login_username_label = tk.Label(app, text="Username")
    login_username_label.pack(pady=5)
    login_username_entry = ctk.CTkEntry(app)
    login_username_entry.pack(pady=5)

    login_password_label = tk.Label(app, text="Password")
    login_password_label.pack(pady=5)
    login_password_entry = ctk.CTkEntry(app, show="*")
    login_password_entry.pack(pady=5)

    def process_login():
        username = login_username_entry.get()
        password = login_password_entry.get()
        if login(username, password):
            messagebox.showinfo("Success", "Logged in successfully!")
            show_main()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    login_process_btn = ctk.CTkButton(app, text="Login", command=process_login, bg_color="#2E7BFF")
    login_process_btn.pack(pady=10)

    back_btn = ctk.CTkButton(app, text="Back", command=show_main, bg_color="#D3D3D3")
    back_btn.pack(pady=10)

def show_main():
    for widget in app.winfo_children():
        widget.destroy()

    login_btn = ctk.CTkButton(app, text="Login", command=show_login, bg_color="#2E7BFF")
    login_btn.pack(pady=20, padx=100, fill="both")

    signup_btn = ctk.CTkButton(app, text="Sign Up", command=show_signup, bg_color="#FF5733")
    signup_btn.pack(pady=20, padx=100, fill="both")

# Main app window
app = tk.Tk()
app.title("Authentication System")
app.geometry("600x400")

show_main()

app.mainloop()
