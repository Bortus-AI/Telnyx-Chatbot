# Telnyx Chat Interface

An interactive chat application that allows conversations with AI models, utilizing the Telnyx API and supporting OpenAI models.

<img width="800" img height="600" alt="Chat Application Interface" src="https://github.com/Bortus-AI/Telnyx-Chatbot/assets/100248124/b566715a-71d5-47b2-8737-c2ea75c6fc55">

## Description

The Telnyx Chat Interface is a graphical chat application designed to interact with multiple AI models through the Telnyx API. It provides a user-friendly environment for real-time chatting with AI entities. The application is developed using Python's Tkinter library for the graphical user interface and incorporates threading to manage API requests asynchronously, ensuring a responsive user experience.

### Features

- Securely save and configure API keys for Telnyx and OpenAI within the application.
- Select from a variety of AI models, including the latest ones from OpenAI.
- Engage in an interactive chat experience with a viewable message history.
- Real-time messaging and response display from AI models.
- Capability to interrupt the AI's responses at any given time.

## AI Models

The application supports a diverse array of AI models, which now includes OpenAI's models, providing users with a broad range of conversational abilities:

- `meta-llama/Llama-2-13b-chat-hf` - A general-purpose chat model.
- `mistralai/Mistral-7B-Instruct-v0.1` - A model tuned for instruction-based interactions.
- `Trelis/Llama-2-7b-chat-hf-function-calling-v2` - A model with the capability to call functions.
- `openai/gpt-3.5-turbo` - OpenAI's efficient language model suitable for a variety of tasks.
- `openai/gpt-3.5-turbo-16k` - An extended context version of GPT-3.5 Turbo.
- `openai/gpt-4` - OpenAI's state-of-the-art AI model.
- `openai/gpt-4-32k` - A GPT-4 variant designed for handling extended token limits.

## Installation

To set up the application, you must have Python and `pip` installed. Follow these steps to install the necessary dependencies:

```bash
pip install requests cryptography
pip install requests requests
```

## Usage

To start the application, run the following command:

```bash
python telnyx_chat.py
```

Make sure to place the `api_keys.txt` file in the same directory as the script or set the API keys through the application interface for both Telnyx and OpenAI.

### Setting the API Keys

1. Navigate to 'File' > 'Set Telnyx/OpenAI API Key'.
2. Enter your respective API keys when prompted.
3. The application will store the keys for subsequent use.

## Configuration

The AI model can be selected from the dropdown menu within the application before initiating a conversation.

## Contributing

If you're interested in contributing, fork the repository and submit a pull request with your proposed changes.

## License

This project is released as open-source under the [MIT License](LICENSE).

## Disclaimer

This software is for educational purposes only. Be sure to adhere to the terms of service for Telnyx and OpenAI when using their APIs.
