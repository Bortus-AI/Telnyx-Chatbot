# Telnyx Chat Interface

An interactive chat application with an AI backend using Telnyx API.

<img width="600" img height="520" alt="image" src="https://github.com/Bortus-AI/Telnyx-Chatbot/assets/100248124/b566715a-71d5-47b2-8737-c2ea75c6fc55">




## Description

This application is a simple chat interface that integrates with the Telnyx API to enable users to have conversations with an AI model. It is built using Python's Tkinter library for the GUI and uses threading to handle API requests without freezing the UI.

### Features

- Set and store API key securely.
- Choose between multiple AI models.
- Interactive chat interface with history viewing.
- Send messages to AI and view responses in real-time.
- Stop AI responses at any time.

## AI Models

The application supports several AI models, which you can select from within the interface. Here are the available models:

- `meta-llama/Llama-2-13b-chat-hf` - A capable and general-purpose chat model.
- `mistralai/Mistral-7B-Instruct-v0.1` - A model fine-tuned for following instructions.
- `Trelis/Llama-2-7b-chat-hf-function-calling-v2` - A specialized model that can call functions.

## Installation

Before running the application, make sure you have Python and `pip` installed on your system. Then, install the required dependencies:

```bash
pip install requests
```

## Usage

To run the AI Chat Interface, execute the Python script with:

```bash
python telnyx_chat.py
```

Make sure you have the `api_key.txt` file in the same directory as the script or set the API key through the interface.

### Setting the API Key

When you first run the application, you will need to set your Telnyx API key:

1. Go to 'File' > 'Set API Key'.
2. Enter your API key in the prompt.
3. The key will be saved for future sessions.

### Sending Messages

1. Type your message in the bottom text area.
2. Press `Enter` to send the message (or `Shift+Enter` for a new line).
3. The AI response will appear in the chat history above.

## Configuration

You can choose the AI model by selecting it from the dropdown menu before sending a message.

## Contributing

Contributions to the AI Chat Interface are welcome! Please fork the repository and create a pull request with your changes or improvements.

## License

This project is open-source and available under the [License](LICENSE).

## Disclaimer

This application is intended for educational purposes only. Usage of the Telnyx API is subject to their terms of service.

