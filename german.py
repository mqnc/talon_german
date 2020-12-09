
import talon
from talon import Context, Module, actions, ui, app, speech_system

mod = Module()
mod.mode('german')

ctx = Context()
ctx.matches = 'mode: user.german'
ctx.settings = {
	'speech.engine': 'vosk',
#	'speech.language': 'de_DE',
	'speech.timeout': 0.3
}

@mod.capture(rule='weg+')
def weg(m) -> str:
	"""capture multiple "weg"s"""
	return m

@mod.action_class
class Actions:
	def smart_insert(txt:str):
		"""context-aware insertion"""

		if actions.edit.selected_text() != "":
			actions.key("backspace")

		actions.edit.extend_left()
		before = actions.edit.selected_text()
		if before != "":
			actions.edit.extend_right()

		actions.edit.extend_right()
		after = actions.edit.selected_text()
		if after != "":
			actions.edit.extend_left()

		actions.insert(txt)

	def smart_delete(txt:str):
		"""delete word and optionally space"""

		for i in range(len(str(txt).split())):

			# first just delete all spaces until next word
			actions.edit.extend_word_left()
			before = actions.edit.selected_text()
			if before != '' and before[-1] in [" ", "\n"]:
				actions.edit.extend_word_right()
				actions.key("backspace")
				continue

			# if there were none, delete next word
			actions.key("backspace")

			# delete spaces before that as well
			actions.edit.extend_left()
			before = actions.edit.selected_text()
			if before in [" ", "\n"]:
				actions.key("backspace")
			elif before != '':
				actions.edit.extend_right()
