import os
import threading
import sys
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig

user_name = "Sak"
schedule = "Gym with Wil at 5:00 p.m."
prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

client = ElevenLabs(api_key=API_KEY)
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
)


def print_agent_response(response):
    print(f"Agent: {response}")


def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")


def print_user_transcript(transcript):
    print(f"User: {transcript}")


conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

def run_session():
    conversation.start_session()

t = threading.Thread(target=run_session, daemon=True)
t.start()

print(" Talking to agent.")
print("Press [ENTER] to stop (or wait for auto-timeout).")

try:
    # Manual stop with ENTER
    input()
    print("\n[!] Stopping conversation…")
    conversation.end_session()
    t.join(timeout=5)
except KeyboardInterrupt:
    print("\n[!] Keyboard interrupt — stopping…")
    conversation.end_session()
    t.join(timeout=5)

# Optional auto-timeout (uncomment if you want)
# import time
# time.sleep(120)
# if t.is_alive():
#     print("\n[!] Auto-timeout — stopping…")
#     conversation.end_session()
#     t.join(timeout=5)

print("Session ended.")
sys.exit(0)