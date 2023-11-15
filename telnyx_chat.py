# Import necessary libraries
import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, Label, OptionMenu, Frame, Button, Text, Scrollbar, Scale
from tkinter import END, DISABLED, NORMAL
import requests
import threading
import json
import os
import base64
import cryptography
from cryptography.fernet import Fernet

# Define the API URL constant
API_URL = "https://api.telnyx.com/v2/ai/generate_stream"

# Define the main application class
class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Chat Interface")  # Set the window title
        self.geometry("800x600")  # Set the default window size
        self.api_key = None  # Variable to store the Telnyx API key
        self.openai_api_key = None  # Variable to store the OpenAI API key
        self.model = tk.StringVar(value="meta-llama/Llama-2-13b-chat-hf")  # Variable to store the selected AI model
        self.stop_event = threading.Event()  # Event to signal when to stop the bot
        self.bot_active = False  # Flag to indicate if the bot is currently active
        self.max_tokens = tk.IntVar(value=128)  # Variable to store the maximum number of tokens for the AI response
        self.temperature = tk.DoubleVar(value=0.9)  # Variable to store the temperature setting for the AI response
        self.init_gui()  # Initialize the graphical user interface
        self.load_api_keys()  # Load the API keys from a file

    def init_gui(self):
        # Initialize the graphical user interface components
        self.menu_bar = Menu(self)  # Create the menu bar
        self.config(menu=self.menu_bar)  # Add the menu bar to the window

        file_menu = Menu(self.menu_bar, tearoff=False)  # Create the file menu
        self.menu_bar.add_cascade(label="File", menu=file_menu)  # Add the file menu to the menu bar
        file_menu.add_command(label="Set Telnyx API Key", command=lambda: self.on_set_api_key('telnyx'))  # Add command to set Telnyx API key
        file_menu.add_command(label="Set OpenAI API Key", command=lambda: self.on_set_api_key('openai'))  # Add command to set OpenAI API key
        file_menu.add_separator()  # Add a separator to the menu
        file_menu.add_command(label="Exit", command=self.on_exit)  # Add command to exit the application

        self.chat_history = Text(self, state=DISABLED, wrap='word')  # Create the chat history text area
        self.chat_history.pack(pady=5, expand=True, fill='both')  # Pack the chat history text area into the window

        chat_scrollbar = Scrollbar(self, command=self.chat_history.yview)  # Create a scrollbar for the chat history
        chat_scrollbar.pack(side=tk.RIGHT, fill='y')  # Pack the scrollbar into the window
        self.chat_history['yscrollcommand'] = chat_scrollbar.set  # Attach the scrollbar to the chat history

        model_label = Label(self, text="Select Model:")  # Create a label for the model selection
        model_label.pack()  # Pack the label into the window
        self.model_dropdown = OptionMenu(self, self.model, "mistralai/Mistral-7B-Instruct-v0.1", 
                                        "meta-llama/Llama-2-13b-chat-hf", 
                                        "Trelis/Llama-2-7b-chat-hf-function-calling-v2", 
                                        "openai/gpt-3.5-turbo", 
                                        "openai/gpt-3.5-turbo-16k", 
                                        "openai/gpt-4", 
                                        "openai/gpt-4-32k")  # Create a dropdown menu for selecting the AI model
        self.model_dropdown.pack()  # Pack the dropdown menu into the window

        self.input_text = Text(self, height=4)  # Create the input text area
        self.input_text.pack(pady=5, expand=True, fill='both')  # Pack the input text area into the window
        self.input_text.bind("<Return>", self.on_send)  # Bind the Return key to the send message event
        self.input_text.bind("<Shift-Return>", self.insert_newline)  # Bind the Shift+Return key to insert a newline

        button_frame = Frame(self)  # Create a frame for the buttons
        button_frame.pack(side=tk.BOTTOM, fill='x', expand=True)  # Pack the button frame into the window

        self.stop_button = Button(button_frame, text="Stop Bot", command=self.on_stop, width=10)  # Create a stop button
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5, fill='x', expand=True)  # Pack the stop button into the button frame

        spacer_frame = Frame(button_frame)  # Create a spacer frame to push buttons apart
        spacer_frame.pack(side=tk.LEFT, expand=True, fill='both')  # Pack the spacer frame into the button frame

        self.send_button = Button(button_frame, text="Send", command=self.on_send, width=10)  # Create a send button
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5, fill='x', expand=True)  # Pack the send button into the button frame

        advanced_settings_frame = Frame(self)  # Create a frame for advanced settings
        advanced_settings_frame.pack(side=tk.BOTTOM, fill='x', expand=True)  # Pack the advanced settings frame into the window

        max_tokens_label = Label(advanced_settings_frame, text="Max Tokens:")  # Create a label for max tokens setting
        max_tokens_label.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the max tokens label into the advanced settings frame
        max_tokens_scale = Scale(advanced_settings_frame, from_=10, to=1024, orient=tk.HORIZONTAL, variable=self.max_tokens, length=200)  # Create a scale for max tokens
        max_tokens_scale.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the max tokens scale into the advanced settings frame

        temperature_label = Label(advanced_settings_frame, text="Temperature:")  # Create a label for temperature setting
        temperature_label.pack(side=tk.RIGHT, padx=5, pady=5)  # Pack the temperature label into the advanced settings frame
        temperature_scale = Scale(advanced_settings_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=self.temperature, length=200)  # Create a scale for temperature
        temperature_scale.pack(side=tk.RIGHT, padx=5, pady=5)  # Pack the temperature scale into the advanced settings frame

    def on_exit(self):
        # Exit the application cleanly
        self.clipboard_clear()  # Clear the clipboard
        self.destroy()  # Destroy the main window

    def load_api_keys(self):
        # Load API keys from a file
        try:
            if os.path.isfile('api_keys.txt'):
                with open('api_keys.txt', 'rb') as file:
                    data = file.read()  # Read the encrypted data from the file
                    fernet = Fernet(self.get_fernet_key())  # Create a Fernet object with the encryption key
                    decrypted_data = fernet.decrypt(data)  # Decrypt the data
                    api_keys = json.loads(decrypted_data)  # Load the decrypted data into a dictionary
                    self.api_key = api_keys.get('telnyx')  # Get the Telnyx API key from the dictionary
                    self.openai_api_key = api_keys.get('openai')  # Get the OpenAI API key from the dictionary
        except Exception as e:
            messagebox.showerror("Error", f"Error loading API keys: {e}")  # Show an error message if there is a problem loading the keys

    def save_api_keys(self):
        # Save API keys to a file
        try:
            with open('api_keys.txt', 'wb') as file:
                api_keys = {
                    'telnyx': self.api_key,  # Store the Telnyx API key
                    'openai': self.openai_api_key  # Store the OpenAI API key
                }
                fernet = Fernet(self.get_fernet_key())  # Create a Fernet object with the encryption key
                encrypted_data = fernet.encrypt(json.dumps(api_keys).encode('utf-8'))  # Encrypt the API keys
                file.write(encrypted_data)  # Write the encrypted data to the file
        except Exception as e:
            messagebox.showerror("Error", f"Error saving API keys: {e}")  # Show an error message if there is a problem saving the keys

    def on_set_api_key(self, api_type):
        # Set an API key
        api_key = simpledialog.askstring("API Key", f"Enter your {api_type.capitalize()} API Key:", parent=self)  # Show a dialog to enter the API key
        if api_key:
            if api_type == 'telnyx':
                self.api_key = api_key  # Set the Telnyx API key
            elif api_type == 'openai':
                self.openai_api_key = api_key  # Set the OpenAI API key
            self.save_api_keys()  # Save the API keys to a file
            self.insert_message(f"Bot: {api_type.capitalize()} API key set successfully.\n")  # Insert a message indicating the key was set

    def on_send(self, event=None):
        # Send a message to the AI model and handle the response
        if event and event.state & 0x0001:  # Check for Shift key
            return  # Allow default text widget behavior (insert newline)
        message = self.input_text.get("1.0", END).strip()  # Get the input message
        if message and self.api_key:
            if not self.bot_active:
                self.bot_active = True  # Set the bot to active
                self.send_button.config(state=DISABLED)  # Disable the send button
                self.insert_message(f"\n\n👤 {message}\n\n")  # Insert the user message into the chat history
                self.insert_message("⚙️\n")  # Insert gear icon before bot response
                self.stop_event.clear()  # Clear the stop event
                threading.Thread(target=self.send_message, args=(message,)).start()  # Start a new thread to send the message
                self.input_text.delete("1.0", END)  # Clear the input after sending
            else:
                messagebox.showinfo("Bot Active", "Please wait for the bot to finish responding.")  # Show a message if the bot is already active
        elif not self.api_key:
            messagebox.showinfo("API Key", "Please set your API key first.")  # Show a message if the API key is not set
        else:
            messagebox.showinfo("Empty Message", "Please enter a message to send.")  # Show a message if the input message is empty
        
        if event:
            return "break"  # Prevents the default behavior of the Enter key

    def insert_newline(self, event=None):
        # Insert a newline in the input text area when Shift+Enter is pressed
        self.input_text.insert(END, "\n")
        return "break"  # Prevents the default behavior of the Shift+Enter key

    def on_stop(self):
        # Stop the AI bot and enable the send button
        self.stop_event.set()  # Set the stop event
        self.insert_message("Bot: Stopped.\n")  # Insert a message indicating the bot has stopped
        self.bot_active = False  # Set the bot to inactive
        self.send_button.config(state=NORMAL)  # Re-enable the send button

    def insert_message(self, message):
        # Insert a message in the chat history text area
        self.chat_history.config(state=NORMAL)  # Enable the chat history text area
        self.chat_history.insert(END, message)  # Insert the message
        self.chat_history.config(state=DISABLED)  # Disable the chat history text area
        self.chat_history.see(END)  # Scroll to the end of the chat history

    def send_message(self, text):
        # Send a message to the AI model using the Telnyx API
        headers = {
            "Authorization": f"Bearer {self.api_key}",  # Set the Authorization header with the API key
            "Content-Type": "application/json"  # Set the Content-Type header to application/json
        }
        data = {
            "text": [text],  # The text to send to the AI model
            "model": self.model.get(),  # The AI model to use
            "max_tokens": self.max_tokens.get(),  # The maximum number of tokens for the AI response
            "temperature": self.temperature.get(),  # The temperature setting for the AI response
            "openai_api_key": self.openai_api_key  # The OpenAI API key if using an OpenAI model
        }
        try:
            with requests.post(API_URL, headers=headers, json=data, stream=True) as response:
                for line in response.iter_lines():
                    if self.stop_event.is_set():
                        break  # Stop if the stop event is triggered
                    if line:
                        decoded_line = line.decode('utf-8')  # Decode the line from the response
                        if decoded_line.startswith('data: '):
                            content = decoded_line.split('data: ', 1)[1]  # Extract the content from the line
                            try:
                                message_data = json.loads(content)  # Parse the content as JSON
                                token = message_data.get('token')  # Get the token from the JSON data
                                if token:
                                    self.insert_message(token)  # Insert the token into the chat history
                                else:
                                    print("Token not found in the response")  # Print an error message if the token is not found
                            except json.JSONDecodeError as e:
                                print("Error decoding JSON response:", e)  # Print an error message if there is a problem decoding the JSON
        except requests.RequestException as e:
            if not self.stop_event.is_set():
                messagebox.showerror("Error", f"Error sending request to API: {e}")  # Show an error message if there is a problem sending the request
        finally:
            self.bot_active = False  # Set the bot to inactive
            self.send_button.config(state=NORMAL)  # Re-enable the send button

    def get_fernet_key(self):
        # Get or generate a Fernet encryption key
        key_file = 'fernet_key.txt'  # The file where the Fernet key is stored
        if not os.path.isfile(key_file):
            key = Fernet.generate_key()  # Generate a new Fernet key
            with open(key_file, 'wb') as file:
                file.write(key)  # Write the key to the file
        else:
            with open(key_file, 'rb') as file:
                key = file.read()  # Read the key from the file
        return key  # Return the key

# Main execution...
if __name__ == "__main__":
    app = ChatApplication()  # Create an instance of the ChatApplication class
    app.mainloop()  # Start the main event loop of the application
