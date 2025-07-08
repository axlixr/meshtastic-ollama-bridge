# Meshtastic to Ollama LLM Chat Bridge

## Overview

This Python script acts as a seamless bridge between a Meshtastic LoRa mesh network and a locally hosted Ollama large language model (LLM). It listens for messages on the mesh that begin with the prefix **@ai**, forwards those prompts to the Ollama LLM for processing, and returns the AI-generated responses directly to the sender node over the mesh.

Designed for simplicity and reliability, this tool enables users to interact with powerful AI models even in remote or offline mesh network environments where traditional internet access is unavailable. It's ideal for adding intelligent, conversational capabilities to decentralized, low-bandwidth communication setups.

<img src="/img/img1.png" alt="Meshtastic to Ollama LLM Chat Bridge Image 1" width="525px">
<img src="/img/img2.jpeg" alt="Meshtastic to Ollama LLM Chat Bridge Image 2" width="525px">


## Features

- Connects to a Meshtastic node over serial USB
- Filters incoming messages to process only those beginning with **@ai**
- Sends prompts to Ollama LLM via HTTP API
- Handles errors and timeouts gracefully
- Sanitizes and trims AI responses to fit Meshtastic message size limits
- Sends AI responses directly back to the sender node
- Logs all important events with timestamps
- Gracefully shuts down on user interrupt

## How It Works

1. **Connecting**: The script connects to the Meshtastic node over serial USB
2. **Listening**: It listens indefinitely for incoming messages on the mesh network
3. **Filtering**: When a message is received, it checks if the text starts with the prefix **@ai**
4. **Prompt Processing**: If yes, the prefix is stripped, and the remaining text is sent as a prompt to the Ollama LLM
5. **LLM Response**: The LLM response is received, sanitized to ASCII characters, trimmed to 200 characters, and sent back over the mesh network to the original sender node
6. **Logging**: Events such as message receipt, API calls, errors, and sends are printed with timestamps
7. **Shutdown**: On Ctrl+C, the script cleanly closes the serial interface and exits
8. **Communication**: Configure your model or prompts to keep responses short, as Meshtastic messages have a 200-byte limit and LLMs often generate lengthy replies *(optional)*

## Requirements

- Python 3.7+
- **Python packages**:
  - `meshtastic`
  - `requests`
  - `pypubsub` (for `pubsub`)
- A Meshtastic node connected via USB
- An Ollama LLM model (default `"llama2"`)
- Ollama LLM API running locally and accessible at `http://[server-ip]:11434/api/generate`

## Installation & Configuration

See [Ollama](https://github.com/ollama/ollama/blob/main/README.md) on how to download and serve a local LLM.

- **OLLAMA_MODEL**: Set the desired Ollama model name the model you serve (default is `"llama2"`)

**Ensure your Meshtastic device is connected via USB.**

```bash
git clone https://github.com/wasted-alien/meshtastic-ollama-bridge.git
cd meshtastic-ollama-bridge
```

```bash
pip install meshtastic requests pypubsub
```

```bash
python main.py
```

Wait for messages. When a mesh node sends a message starting with **@ai**, e.g.:

```bash
@ai Hello how are you LLM?
```

The script will query Ollama and directly reply back to the sender node with the AI's answer.

## License & Attribution

GNU General Public License v3.0

Created by **Wasted Alien.**

**Disclaimer:** This is an unofficial project and is not affiliated with or endorsed by the Meshtastic team.

## Acknowledgments

- [Meshtastic](https://meshtastic.org) – Mesh communication platform
- [Meshtastic Python API](https://github.com/meshtastic/meshtastic-python) – For direct serial communication with the mesh
- [Ollama](https://ollama.com/) – Get up and running with large language models
