import tkinter as tk
from tkinter import messagebox, scrolledtext
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Chat history
history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
    {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
]

# Function to connect to the server
def connect_to_server():
    global history
    try:
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message["content"] += chunk.choices[0].delta.content

        history.append(new_message)
        display_message("assistant", new_message["content"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")

# Function to handle user input
def send_message():
    global history
    user_message = user_input.get()
    if user_message.strip():
        display_message("user", user_message)
        history.append({"role": "user", "content": user_message})
        user_input.delete(0, tk.END)
        connect_to_server()

# Set up the main window
root = tk.Tk()
root.title("CatGPT 1.0.0 Ask Anything")
root.geometry("600x400")

# Disable maximize button
root.resizable(False, False)

# Set up the response text area
response_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
response_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Set up the user input field
user_input = tk.Entry(root, width=50)
user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=10)

# Set up the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Set up the connect button (disabled)
connect_button = tk.Button(root, text="Connect to Server", state=tk.DISABLED)
connect_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Function to display text in the response_text area
def display_message(role, message):
    response_text.configure(state=tk.NORMAL)
    response_text.insert(tk.END, f"{role.capitalize()}: {message}\n")
    response_text.configure(state=tk.DISABLED)
    response_text.see(tk.END)

# Update the send_message function to display the user message
def send_message():
    global history
    user_message = user_input.get()
    if user_message.strip():
        display_message("user", user_message)
        history.append({"role": "user", "content": user_message})
        user_input.delete(0, tk.END)
        connect_to_server()

# Update the connect_to_server function to display the assistant's response
def connect_to_server():
    global history
    try:
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message["content"] += chunk.choices[0].delta.content

        history.append(new_message)
        display_message("assistant", new_message["content"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")

root.mainloop()
