# Import necessary libraries
import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, Label, OptionMenu, Frame, Button, Text, Scrollbar, Scale
from tkinter import END, DISABLED, NORMAL
import requests
import threading
import json
import os
import base64

# Define the API URL constant
API_URL = "https://api.telnyx.com/v2/ai/generate_stream"

# Define the main application class
class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Chat Interface")  # Set the window title
        self.geometry("800x600")  # Set the window size

        # Initialize variables
        self.api_key = None  # Will hold the API key
        self.model = tk.StringVar(value="meta-llama/Llama-2-13b-chat-hf")  # Default AI model
        self.stop_event = threading.Event()  # Event to signal bot to stop
        self.bot_active = False  # Flag to indicate if bot is currently active

        # Initialize new variables for max_tokens and temperature with their defaults
        self.max_tokens = tk.IntVar(value=128)
        self.temperature = tk.DoubleVar(value=0.9)

        # Setup the GUI components
        self.init_gui()
        # Load the API key if it exists
        self.load_api_key()
    def init_gui(self):
        # Create a menu bar
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # Add 'File' menu to the menu bar
        file_menu = Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Set API Key", command=self.on_set_api_key)  # Add 'Set API Key' option
        file_menu.add_command(label="Exit", command=self.on_exit)  # Add 'Exit' option

        # Create the chat history text area
        self.chat_history = Text(self, state=DISABLED, wrap='word')
        self.chat_history.pack(pady=5, expand=True, fill='both')

        # Create a scrollbar for the chat history and link it
        chat_scrollbar = Scrollbar(self, command=self.chat_history.yview)
        chat_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.chat_history['yscrollcommand'] = chat_scrollbar.set

        # Add a dropdown menu for model selection
        model_label = Label(self, text="Select Model:")
        model_label.pack()
        self.model_dropdown = OptionMenu(self, self.model, "meta-llama/Llama-2-13b-chat-hf", "mistralai/Mistral-7B-Instruct-v0.1", "Trelis/Llama-2-7b-chat-hf-function-calling-v2")
        self.model_dropdown.pack()

        # Create the input text area
        self.input_text = Text(self, height=4)
        self.input_text.pack(pady=5, expand=True, fill='both')
        self.input_text.bind("<Return>", self.on_send)  # Bind the Enter key to send message
        self.input_text.bind("<Shift-Return>", self.insert_newline)  # Bind Shift+Enter to insert newline

        # Create a frame for buttons
        button_frame = Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill='x', expand=True)

        # Add 'Stop Bot' button
        self.stop_button = Button(button_frame, text="Stop Bot", command=self.on_stop, width=10)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5, fill='x', expand=True)

        # Add a spacer frame
        spacer_frame = Frame(button_frame)
        spacer_frame.pack(side=tk.LEFT, expand=True, fill='both')

        # Add 'Send' button
        self.send_button = Button(button_frame, text="Send", command=self.on_send, width=10)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5, fill='x', expand=True)

        # Create a frame for advanced settings
        advanced_settings_frame = Frame(self)
        advanced_settings_frame.pack(side=tk.BOTTOM, fill='x', expand=True)

        # Create a scale for max tokens with increased length
        max_tokens_label = Label(advanced_settings_frame, text="Max Tokens:")
        max_tokens_label.pack(side=tk.LEFT, padx=5, pady=5)
        max_tokens_scale = Scale(advanced_settings_frame, from_=10, to=1024, orient=tk.HORIZONTAL, variable=self.max_tokens, length=200) # Increased length
        max_tokens_scale.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a scale for temperature with increased length
        temperature_scale = Scale(advanced_settings_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.temperature, length=200)  # Increased length
        temperature_scale.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Pack the temperature label to the left of the temperature scale
        temperature_label = Label(advanced_settings_frame, text="Temperature:")
        temperature_label.pack(side=tk.RIGHT, padx=5, pady=5)

    def on_exit(self):
        # Clear the clipboard and close the application
        self.clipboard_clear()
        self.destroy()

    def load_api_key(self):
        # Load the API key from a file if it exists
        try:
            if os.path.isfile('api_key.txt'):
                with open('api_key.txt', 'r') as file:
                    # Decode the encoded API key
                    encoded_api_key = file.read().strip()
                    self.api_key = base64.b64decode(encoded_api_key).decode('utf-8')
                    self.insert_message("Bot: Loaded API key from file.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading API key: {e}")

    def save_api_key(self):
        # Save the API key to a file
        try:
            with open('api_key.txt', 'w') as file:
                # Encode the API key before saving
                encoded_api_key = base64.b64encode(self.api_key.encode('utf-8')).decode('utf-8')
                file.write(encoded_api_key)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving API key: {e}")

    def on_set_api_key(self):
        # Prompt the user to enter an API key and save it
        api_key = simpledialog.askstring("API Key", "Enter your API Key:", parent=self)
        if api_key:
            self.api_key = api_key
            self.save_api_key()
            self.insert_message("Bot: API key set successfully.\n")

    def on_send(self, event=None):
        # Send a message to the AI model and handle the response
        if event and event.state & 0x0001:  # Check for Shift key
            return  # Allow default text widget behavior (insert newline)
        message = self.input_text.get("1.0", END).strip()
        if message and self.api_key:
            if not self.bot_active:
                self.bot_active = True
                self.send_button.config(state=DISABLED)
                self.insert_message(f"\n\n👤 {message}\n\n")
                self.insert_message("⚙️\n")  # Insert gear icon before bot response
                self.stop_event.clear()
                threading.Thread(target=self.send_message, args=(message,)).start()
                self.input_text.delete("1.0", END)  # Clear the input after sending
            else:
                messagebox.showinfo("Bot Active", "Please wait for the bot to finish responding.")
        elif not self.api_key:
            messagebox.showinfo("API Key", "Please set your API key first.")
        else:
            messagebox.showinfo("Empty Message", "Please enter a message to send.")
        
        if event:
            return "break"  # Prevents the default behavior of the Enter key

    def insert_newline(self, event=None):
        # Insert a newline in the input text area when Shift+Enter is pressed
        self.input_text.insert(END, "\n")
        return "break"  # Prevents the default behavior of the Shift+Enter key

    def on_stop(self):
        # Stop the AI bot and enable the send button
        self.stop_event.set()
        self.insert_message("Bot: Stopped.\n")
        self.bot_active = False
        self.send_button.config(state=NORMAL)

    def insert_message(self, message):
        # Insert a message in the chat history text area
        self.chat_history.config(state=NORMAL)
        self.chat_history.insert(END, message)
        self.chat_history.config(state=DISABLED)
        self.chat_history.see(END)

    def send_message(self, text):
        # Send the user message to the API and process the response
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "text": [text],
            "model": self.model.get(),
            "max_tokens": self.max_tokens.get(),  # Add max_tokens to the request
            "temperature": self.temperature.get()  # Add temperature to the request
        }
        try:
            with requests.post(API_URL, headers=headers, json=data, stream=True) as response:
                for line in response.iter_lines():
                    if self.stop_event.is_set():
                        break  # Stop if the stop event is triggered
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data: '):
                            content = decoded_line.split('data: ', 1)[1]
                            try:
                                message_data = json.loads(content)
                                token = message_data.get('token')
                                if token:
                                    self.insert_message(token)
                                else:
                                    print("Token not found in the response")
                            except json.JSONDecodeError as e:
                                print("Error decoding JSON response:", e)
        except requests.RequestException as e:
            if not self.stop_event.is_set():
                messagebox.showerror("Error", f"Error sending request to API: {e}")
        finally:
            self.bot_active = False  # Set the bot to inactive
            self.send_button.config(state=NORMAL)  # Re-enable the send button

# Main execution: create an instance of the application and start the main loop
if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
