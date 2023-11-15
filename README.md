# Telnyx Chat Interface

An interactive chat application with an AI backend using Telnyx API.

<img width="600" img height="520" alt="image" src="https://github.com/Bortus-AI/Telnyx-Chatbot/assets/100248124/b566715a-71d5-47b2-8737-c2ea75c6fc55">

## Description

This application is a simple chat interface that integrates with the Telnyx API and now also supports OpenAI models. It enables users to have conversations with various AI models. The app is built using Python's Tkinter library for the GUI and uses threading to handle API requests without freezing the UI.

### Features

- Set and store API keys securely for both Telnyx and OpenAI.
- Choose between multiple AI models including OpenAI's latest offerings.
- Interactive chat interface with history viewing.
- Send messages to AI and view responses in real-time.
- Stop AI responses at any time.

## AI Models

The application now supports a range of AI models, including those from OpenAI. Here are the available models:

- `meta-llama/Llama-2-13b-chat-hf` - A capable and general-purpose chat model.
- `mistralai/Mistral-7B-Instruct-v0.1` - A model fine-tuned for following instructions.
- `Trelis/Llama-2-7b-chat-hf-function-calling-v2` - A specialized model that can call functions.
- `openai/gpt-3.5-turbo` - OpenAI's versatile and efficient language model.
- `openai/gpt-3.5-turbo-16k` - An extended version of GPT-3.5 Turbo for longer context.
- `openai/gpt-4` - The latest and most advanced AI model from OpenAI.
- `openai/gpt-4-32k` - A variant of GPT-4 with an extended token limit.

## Installation

Before running the application, ensure Python and `pip` are installed on your system. Then, install the required dependencies:

```bash
pip install requests
```

## Usage

To run the AI Chat Interface, execute:

```bash
python telnyx_chat.py
```

Ensure you have the `api_key.txt` file in the same directory as the script or set the API key through the interface for both Telnyx and OpenAI.

### Setting the API Key

1. Go to 'File' > 'Set API Key'.
2. Enter your Telnyx and OpenAI API keys in the prompt.
3. The keys will be saved for future sessions.

## Configuration

You can choose the AI model by selecting it from the dropdown menu before sending a message.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes or improvements.

## License

This project is open-source and available under the [License](LICENSE).

## Disclaimer

This application is intended for educational purposes only. Usage of the Telnyx and OpenAI APIs is subject to their respective terms of service.
