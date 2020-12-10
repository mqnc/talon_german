
import talon
from talon import Context, Module, actions, ui, app, speech_system
import unicodedata

mod = Module()
mod.mode('german')

ctx = Context()
ctx.matches = 'mode: user.german'
ctx.settings = {
	'speech.engine': 'vosk',
#	'speech.language': 'de_DE',
	'speech.timeout': 0.3
}

mod.list("buchstabe", desc="The spoken phonetic alphabet")
ctx.lists["self.buchstabe"] = {
	"alpha": "a",
	"bravo": "b",
	"charlie": "c",
	"delta": "d",
	"echo": "e",
	"foxtrott": "f",
	"golf": "g",
	"hotel": "h",
	"india": "i",
	"julia": "j",
	"kilo": "k",
	"lima": "l",
	"mike": "m",
	"november": "n",
	"oskar": "o",
	"papa": "p",
	"québec": "q",
	"romeo": "r",
	"sierra": "s",
	"tango": "t",
	"uniform | uniformen": "u",
	"viktor": "v",
	"whisky": "w",
	"x ray": "x",
	"junkie": "y",
	"zulu": "z",
	"ära": "ä",
	"ökonom | ökonomen": "ö",
	"übermut": "ü",
	"s z": "ß",
}

mod.list("sonderzeichen", desc="Special symbols")
ctx.lists["self.sonderzeichen"] = {
	"leerzeichen": "␣", # will become spaces after all substitutions
	"blank": "␣",
	"blink": "␣",
	"plenk": "␣",
	"planck": "␣",
	"punkt": ".",
	"beistrich": ",", # komma is often confused with komme
	"fragezeichen": "?",
	"ausrufezeichen": "!",
	"doppelpunkt": ":",
	"semikolon": ";",
	"bindestrich": "-",
	"unterstrich": "_",
	"schrägstrich": "/",
	"backslash": "\\",
	"senkrecht strich": "|",
	"zitat": '"',
	"zitat ende": '" ',
	"apostroph": "'",
	"klammer auf": "(",
	"klammer zu": ")",
	"eckige klammer auf": "[",
	"eckige klammer zu": "]",
	"geschweifte klammer auf": "{",
	"geschweifte klammer zu": "}",
	"at | klammeraffe": "@",
	"dollar": "$",
	"und zeichen": "&",
	"sternchen": "*",
	"kleiner zeichen": "<",
	"größer zeichen": ">",
	"ist gleich zeichen": "=",
	"raute": "#",
	"tilde": "~",
	"zirkumflex": "^",
}

_space_after = ".,!?:;)]}"
_no_space_before = ".,!?:;)]}␣"

mod.list("modifier", desc="Modifiers for upper casement")
ctx.lists["self.modifier"] = {
	"hoch": "CAP", # groß often becomes große/großer/großes
	"huch": "CAP",
	"alles hoch": "ALLCAPS",
}

@mod.capture(rule='({self.buchstabe}+) | <word>')
def wort(m) -> str:
	"""word or spelled word, inserts space in the end"""
	return ''.join(str(m).split()) + ' '

@mod.capture(rule='[{self.modifier}] <self.wort>')
def gk_wort(m) -> str:
	"""potentially upper case word"""
	if m[0] == "CAP":
		return str(m[1])[0].upper() + str(m[1])[1:]
	elif m[0] == "ALLCAPS":
		return str(m[1]).upper()
	else:
		return str(m)

@mod.capture(rule='<self.gk_wort> | {self.sonderzeichen}')
def satzglied(m) -> str:
	"""word or symbol"""
	if str(m)[0] in _space_after:
		return str(m) + ' '
	else:
		return str(m)

@mod.capture(rule='<self.satzglied>+')
def satz(m) -> str:
	"""sentence"""
	result = [str(m[0])]
	for i in range(1, len(m)):
		if str(m[i])[0] in _no_space_before and result[i-1][-1] == ' ':
			result[i-1] = result[i-1][:-1]
		result.append(str(m[i]))
	result = ''.join(result)

	if result[-1] == ' ':
		result = result[:-1]

	result = result.replace('␣', ' ')
	return result

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

		squeeze_into_word = False
		if before != "" and unicodedata.category(before)[0] == 'L' \
				and after != "" and unicodedata.category(after)[0] == 'L':
			squeeze_into_word = True

		if before != "" \
				and (unicodedata.category(before)[0] == 'L' or before in _space_after) \
				and txt[0] not in _no_space_before \
				and not squeeze_into_word:
			actions.insert(' ')

		actions.insert(txt)

		if after != "" \
				and (txt[-1] in _space_after or unicodedata.category(txt[-1])[0] == 'L')\
				and after not in ' \n\t' \
				and after not in _no_space_before \
				and not squeeze_into_word:
			actions.insert(' ')


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
