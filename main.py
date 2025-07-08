import meshtastic
import meshtastic.serial_interface
import requests
import time
from pubsub import pub
from datetime import datetime

OLLAMA_MODEL = "llama2" # Change this to your desired model if needed

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def ask_ollama(prompt, model="llama2"): # Change model if needed
    url = "http://[server-ip]:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("response", "No response.")
    except Exception as e:
        log(f"❌ Error calling Ollama: {e}")
        return "Sorry, I couldn't process your request."

def sanitize_text(text):
    # Keep ASCII only, remove newlines, trim whitespace
    ascii_text = ''.join(c for c in text if 32 <= ord(c) <= 126)
    return ascii_text.strip()

def on_receive(packet):
    if "decoded" in packet and "text" in packet["decoded"]:
        incoming_text = packet["decoded"]["text"]
        sender = packet.get("from", None)
        log(f"📩 Received from {sender}: {incoming_text}")

        # Only process messages starting with '@ai'
        if not incoming_text.lower().startswith("@ai"):
            log("⏭ Message does not start with @ai — ignoring.")
            return

        # Remove the '@ai' prefix before sending prompt to the model
        prompt = incoming_text[3:].strip()

        if not prompt:
            log("⚠️ Empty prompt after @ai, ignoring.")
            return

        # Get LLM response
        response = ask_ollama(prompt)
        log(f"🤖 LLM response: {response}")

        # Sanitize and trim response to 200 chars (Meshtastic max payload ~240 bytes)
        response = sanitize_text(response)[:200]

        if sender and isinstance(sender, int):
            try:
                log(f"🚀 Sending response to node ID: {sender}")
                interface.sendText(response, destinationId=sender)
                log("✅ Response sent over mesh.")
            except Exception as e:
                log(f"❌ Failed to send response: {e}")
        else:
            log(f"⚠️ Invalid sender ID: {sender}")

def main():
    global interface
    log("🔌 Connecting to Meshtastic node...")
    interface = meshtastic.serial_interface.SerialInterface()

    pub.subscribe(on_receive, "meshtastic.receive")

    log("🕒 Waiting for messages... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("🛑 Exiting.")
    finally:
        interface.close()

if __name__ == "__main__":
    main()
