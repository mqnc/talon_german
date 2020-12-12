# Talon German
German Dictation Mode for Talon Voice

## Status
This is the first prototype, don't expect a highly satisfying user experience.

## Dependencies
This is a plug-in for (so far only the patreon-only beta version of) Talon Voice (https://talonvoice.com/).

## Setup
* download the German language model from https://alphacephei.com/vosk/models/vosk-model-de-0.6.zip and extract it into `~/.talon/vosk/`
* run `~/.talon/bin/pip install vosk` (on windows `scripts\pip install vosk`)
* clone this repository into your talon user folder

It won't work on mac unless you sign the pip installed library file yourself, or unless aegis ships the vosk kaldi library with talon pre-signed.

## Usage
Say "german" to switch from command mode to German dictation mode and "english/englisch" to switch back. Check out the german.talon and german.py files for German commands.

## Contribute
Feel free to report issues or discuss things on Slack: https://talonvoice.com/chat #language-deutsch
