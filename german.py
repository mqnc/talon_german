
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

@mod.capture(rule="<phrase>")
def diktat(m) -> str:
	"""german dictation"""
	return str(m)

@mod.capture(rule="<word>")
def wort(m) -> str:
	"""german dictation"""
	return str(m)

@mod.action_class
class Actions:
	def smart_insert(txt:str):
		"""context-aware insertion"""
		print(">", txt, "<")
		'''
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

		actions.insert(txt)'''
