import pyperclip
from auth import create_master_password, verify_master_password
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

from database import (
    create_database,
    add_password,
    get_passwords,
    search_passwords,
    update_password,
    delete_password
)

from encryption import (
    generate_key,
    encrypt_password,
    decrypt_password
)
from password_generator import generate_password


# Initialize database and encryption
generate_key()
create_database()


def save_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not username or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    encrypted_password = encrypt_password(password)

    add_password(
        website,
        username,
        encrypted_password
    )

    messagebox.showinfo(
        "Success",
        "Password saved successfully!"
    )

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def generate_new_password():
    password = generate_password(12)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_password():
    password = password_entry.get().strip()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Please generate or enter a password first."
        )
        return

    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )
def view_passwords():
    records = get_passwords()

    if not records:
        messagebox.showinfo(
            "Saved Passwords",
            "No passwords saved yet."
        )
        return

    show_records(records)


def search_saved_passwords():
    website = search_entry.get().strip()

    if not website:
        messagebox.showwarning(
            "Search",
            "Please enter a website name."
        )
        return

    records = search_passwords(website)

    if not records:
        messagebox.showinfo(
            "Search Result",
            "No matching records found."
        )
        return

    show_records(records)


def show_records(records):
    result = ""

    for record in records:
        record_id, website, username, encrypted_password = record

        password = decrypt_password(encrypted_password)

        result += (
            f"ID: {record_id}\n"
            f"Website: {website}\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
            f"{'-' * 40}\n"
        )

    messagebox.showinfo(
        "Saved Passwords",
        result
    )


def update_saved_password():
    record_id = simpledialog.askinteger(
        "Update Password",
        "Enter the ID of the record to update:"
    )

    if record_id is None:
        return

    records = get_passwords()

    selected_record = None

    for record in records:
        if record[0] == record_id:
            selected_record = record
            break

    if selected_record is None:
        messagebox.showerror(
            "Error",
            "Record ID not found."
        )
        return

    website = simpledialog.askstring(
        "Update",
        "Enter new website:",
        initialvalue=selected_record[1]
    )

    username = simpledialog.askstring(
        "Update",
        "Enter new username:",
        initialvalue=selected_record[2]
    )

    password = simpledialog.askstring(
        "Update",
        "Enter new password:"
    )

    if not website or not username or not password:
        messagebox.showwarning(
            "Update",
            "All fields are required."
        )
        return

    encrypted_password = encrypt_password(password)

    update_password(
        record_id,
        website,
        username,
        encrypted_password
    )

    messagebox.showinfo(
        "Success",
        "Password updated successfully!"
    )


def delete_saved_password():
    record_id = simpledialog.askinteger(
        "Delete Password",
        "Enter the ID of the record to delete:"
    )

    if record_id is None:
        return

    records = get_passwords()

    exists = any(record[0] == record_id for record in records)

    if not exists:
        messagebox.showerror(
            "Error",
            "Record ID not found."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this record?"
    )

    if confirm:
        delete_password(record_id)

        messagebox.showinfo(
            "Success",
            "Password deleted successfully!"
        )


# Main Window
def password_dialog(title, prompt):
    result = {"password": None}

    window = tk.Toplevel()
    window.title(title)
    window.geometry("400x170")
    window.resizable(False, False)

    tk.Label(window, text=prompt).pack(pady=15)

    frame = tk.Frame(window)
    frame.pack()

    entry = tk.Entry(frame, width=30, show="*")
    entry.pack(side="left")

    def toggle_password():
        if entry.cget("show") == "*":
            entry.config(show="")
            eye_button.config(text="🙈")
        else:
            entry.config(show="*")
            eye_button.config(text="👁")

    eye_button = tk.Button(
        frame,
        text="👁",
        command=toggle_password
    )
    eye_button.pack(side="left", padx=5)

    def submit():
        result["password"] = entry.get()
        window.destroy()

    tk.Button(
        window,
        text="OK",
        command=submit
    ).pack(pady=15)

    entry.focus()
    window.grab_set()
    window.wait_window()

    return result["password"]
def authenticate_user():
    # First time setup
    if not os.path.exists("master_salt.bin") or not os.path.exists("master_hash.bin"):

        password = password_dialog(
    "Create Master Password",
    "Create your master password:"
)

        if not password:
            return False

        if len(password) < 8:
            messagebox.showwarning(
                "Weak Password",
                "Master password must be at least 8 characters."
            )
            return False

        confirm_password = password_dialog(
    "Confirm Password",
    "Enter your master password again:"
)

        if password != confirm_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )
            return False

        create_master_password(password)

        messagebox.showinfo(
            "Success",
            "Master password created successfully!"
        )

        return True

    # Existing user login
    for attempt in range(3):

        password = password_dialog(
    "Login",
    "Enter your master password:"
)

        if password is None:
            return False

        if verify_master_password(password):
            return True

        remaining = 2 - attempt

        if remaining > 0:
            messagebox.showerror(
                "Login Failed",
                f"Incorrect password.\nAttempts remaining: {remaining}"
            )

    messagebox.showerror(
        "Access Denied",
        "Too many incorrect attempts."
    )

    return False
root = tk.Tk()
root.geometry("500x750")
root.configure(bg="#f2f2f2")

root.withdraw()

if not authenticate_user():
    root.destroy()
    exit()

root.deiconify()

root.title("Password Manager")
root.geometry("600x720")
root.resizable(False, False)
root.configure(bg="#f5f5f5")


title_label = tk.Label(
    root,
    text="🔐 Password Manager",
    font=("Arial", 26, "bold"),
    bg="#f5f5f5",
    fg="#222222"
)
title_label.pack(pady=20)
button_style = {
    "font": ("Arial", 11, "bold"),
    "bg": "#333333",
    "fg": "white",
    "activebackground": "#555555",
    "activeforeground": "white",
    "relief": "flat",
    "cursor": "hand2"
}


# Website
tk.Label(
    root,
    text="Website / App",
    font=("Arial", 11)
).pack()

website_entry = tk.Entry(
    root,
    width=45
)

website_entry.pack(pady=5)


# Username
tk.Label(
    root,
    text="Username / Email",
    font=("Arial", 11)
).pack()

username_entry = tk.Entry(
    root,
    width=45
)

username_entry.pack(pady=5)


# Password
tk.Label(
    root,
    text="Password",
    font=("Arial", 11)
).pack()

password_entry = tk.Entry(
    root,
    width=45,
    show="*"
)

password_entry.pack(pady=5)
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_button.config(text="🙈 Hide Password")
    else:
        password_entry.config(show="*")
        show_button.config(text="👁 Show Password")


show_button = tk.Button(
    root,
    text="👁 Show Password",
    command=toggle_password,
    width=25,
    **button_style
)

show_button.pack(pady=5)


# Generate Password
tk.Button(
    root,
    text="🎲 Generate Password",
    command=generate_new_password,
    width=25,
    **button_style
).pack(pady=10)
tk.Button(
    root,
    text="📋 Copy Password",
    command=copy_password,
    width=25,
    **button_style
).pack(pady=5)


# Save
tk.Button(
    root,
    text="💾 Save Password",
    command=save_password,
    width=25,
    **button_style
).pack(pady=5)


# View
tk.Button(
    root,
    text="👁 View Saved Passwords",
    command=view_passwords,
    width=25,
     **button_style
).pack(pady=5)


# Search Section
tk.Label(
    root,
    text="Search Website",
    font=("Arial", 11, "bold")
).pack(pady=(20, 5))

search_entry = tk.Entry(
    root,
    width=45
)

search_entry.pack(pady=5)


tk.Button(
    root,
    text="🔍 Search",
    command=search_saved_passwords,
    width=25,
    **button_style
).pack(pady=5)


# Update
tk.Button(
    root,
    text="✏️ Update Password",
    command=update_saved_password,
    width=25,
     **button_style
).pack(pady=5)


# Delete
tk.Button(
    root,
    text="🗑 Delete Password",
    command=delete_saved_password,
    width=25,
     **button_style
).pack(pady=5)


root.mainloop()