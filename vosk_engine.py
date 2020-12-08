
# ideally you integrate this into your engines.py file

from talon import speech_system, Context
from talon.engines.vosk import VoskEngine

vosk_de = VoskEngine(model='vosk-model-de-0.6', language='de_DE')
speech_system.add_engine(vosk_de)

# especially this should not be here but in your engines.py file:
ctx = Context()
ctx.settings = {
    'speech.engine': 'wav2letter', # your default engine goes here
}
