import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import sv_ttk  # Make sure to install sv_ttk

# Mock authentication function
def authenticate(username):
    # This function should contain actual authentication logic
    return "sample_token"  # Mock token

# Function to send file data to API
def send_file(file_path, file_id, file_type, token):
    url = 'https://your-api-endpoint.com/upload'  # Replace with actual URL

    # Preparing headers with the token
    headers = {'Authorization': f'Bearer {token}'}
    
    # Open the file and send it in binary mode
    with open(file_path, 'rb') as file:
        files = {'file': file}
        data = {'id': file_id, 'type': file_type}
        response = requests.post(url, files=files, data=data, headers=headers)

    if response.status_code == 200:
        messagebox.showinfo("Success", "File uploaded successfully!")
    else:
        messagebox.showerror("Error", f"Failed to upload file. Status code: {response.status_code}")

# Main Application Class
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Dark Mode File Upload")
        self.geometry("400x350")

        # Apply dark mode theme
        sv_ttk.set_theme("dark")

        # Variables
        self.token = None
        self.username_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.type_var = tk.StringVar(value="A")  # Default to 'A'
        self.file_path = None

        # Show login screen initially
        self.show_login_screen()

    def show_login_screen(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Main Frame for login
        login_frame = ttk.Frame(self, padding="20")
        login_frame.pack(expand=True)

        # Username Entry
        ttk.Label(login_frame, text="Username:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(login_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, pady=5)

        # Login Button
        ttk.Button(login_frame, text="Login", command=self.login).grid(row=1, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_var.get()
        if username:
            # Mock authentication
            self.token = authenticate(username)
            messagebox.showinfo("Login", f"Logged in with token: {self.token}")
            self.show_upload_screen()
        else:
            messagebox.showwarning("Login", "Please enter a username.")

    def show_upload_screen(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Main Frame for upload form
        upload_frame = ttk.Frame(self, padding="20")
        upload_frame.pack(expand=True)

        # ID Entry
        ttk.Label(upload_frame, text="ID:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(upload_frame, textvariable=self.id_var, width=30).grid(row=0, column=1, pady=5)

        # Type Dropdown
        ttk.Label(upload_frame, text="Type:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        type_options = ["A", "B", "C"]
        ttk.OptionMenu(upload_frame, self.type_var, *type_options).grid(row=1, column=1, pady=5, sticky="w")

        # File Upload Button
        file_frame = ttk.Frame(upload_frame)
        file_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        ttk.Button(file_frame, text="Choose File", command=self.choose_file).pack(side="left")
        self.file_label = ttk.Label(file_frame, text="No file selected", anchor="w")
        self.file_label.pack(side="left", padx=10)

        # Submit Button
        ttk.Button(upload_frame, text="Submit", command=self.submit).grid(row=3, column=0, columnspan=2, pady=20)

        # Configure grid weights to center the layout
        upload_frame.columnconfigure(0, weight=1)
        upload_frame.columnconfigure(1, weight=3)

    def choose_file(self):
        # Open file dialog and store file path
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=f"Selected file: {self.file_path.split('/')[-1]}")  # Display filename only

    def submit(self):
        # Check for required fields
        if not self.file_path:
            messagebox.showwarning("Input Error", "Please select a file.")
            return
        if not self.id_var.get():
            messagebox.showwarning("Input Error", "Please enter an ID.")
            return
        if not self.token:
            messagebox.showwarning("Authentication Error", "Please login first.")
            return

        # Get values
        file_id = self.id_var.get()
        file_type = self.type_var.get()
        
        # Send file with binary input as discussed
        send_file(self.file_path, file_id, file_type, self.token)

# Run the application
if __name__ == "__main__":
    app = Application()
    app.mainloop()