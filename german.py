import talon
from talon import Context, Module, actions, ui, app, speech_system, scope, settings, clip
import unicodedata
import os
import time
from . clipscanner import ClipScanner

# dictionary for capitalization

path = os.path.dirname(os.path.abspath(__file__))
with open(path + "/dictionary/german.dic", encoding='ISO-8859-1') as f:
	list_of_words = f.read().split("\n")

dict_of_words = {}
for word in list_of_words:
	if word.lower() in dict_of_words:
		# multiple entries, use lower
		dict_of_words[word.lower()] = word.lower()
	else:
		dict_of_words[word.lower()] = word


mod = Module()
mod.mode('german')

ctx = Context()
ctx.matches = 'mode: user.german'
ctx.settings = {
	'speech.engine': 'vosk',
	#	'speech.language': 'de_DE',
	'speech.timeout': 0.3
}

mod.setting("german_unicode",
			type=int,
			default=1,
			desc="Enable proper unicode punctuation")

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

mod.list("ziffer", desc="Numbers")
ctx.lists["self.ziffer"] = {
	"null": "0",
	"eins": "1",
	"zwei": "2",
	"drei": "3",
	"vier": "4",
	"fünf": "5",
	"sechs": "6",
	"sieben": "7",
	"acht": "8",
	"neun": "9",
	"komma": ",",
	"punkt": ".",
}

mod.list("sonderzeichen", desc="Special symbols")
ctx.lists["self.sonderzeichen"] = {
	"leerzeichen": "␣",  # will become spaces after all substitutions
	"blank": "␣",
	"blink": "␣",
	"plenk": "␣",
	"planck": "␣",
	"punkt": ".",
	"beistrich": ",",  # komma is often confused with komme
	"bei strich": ",",  # komma is often confused with komme
	"fragezeichen": "?",
	"ausrufezeichen": "!",
	"doppelpunkt": ":",
	"semikolon": ";",
	"bindestrich": "-",
	"gedankenstrich": "–",
	"unterstrich": "_",
	"schrägstrich": "/",
	"backslash": "\\",
	"senkrecht strich": "|",
	"zitat": '„',
	"zitat ende": '“',
	"halbes zitat": '‚',
	"halbes zitat ende": '‘',
	"apostroph": "’",
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

_space_after = ".,!?:;)]}–“‘"
_no_space_before = ".,-!?:;)]}␣“‘’"
_ascii_replace = {'–': '-', '„': '"', '“': '"', "‚": "'", "‘": "'", "’": "'"}
_capitalize_after = ".!?"

mod.list("modifier", desc="Modifiers for upper casement")
ctx.lists["self.modifier"] = {
	"schiff": "CAP",  # groß often becomes große/großer/großes
	"schiffs": "CAP",
	"schifft": "CAP",
	"holzschiff": "ALLCAPS",  # hold shift
	"zwerg": "LOWER",
}


@mod.capture(rule='({self.buchstabe}+) | ({self.ziffer}+) | <word>')
def wort(m) -> str:
	"""word or spelled word or number, inserts space in the end"""
	return ''.join(str(m).split()) + ' '


@mod.capture(rule='[{self.modifier}] <self.wort>')
def gk_wort(m) -> str:
	"""potentially upper case word"""
	if m[0] == "CAP":
		return str(m[1])[0].upper() + str(m[1])[1:]
	elif m[0] == "ALLCAPS":
		return str(m[1]).upper()
	elif m[0] == "LOWER":
		return str(m[1]).lower()
	else:
		word = str(m)
		key = word.replace(" ", "")
		if key in dict_of_words:
			return dict_of_words[key] + " "
		else:
			return word


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
		if str(m[i])[0] in _no_space_before and result[i - 1][-1] == ' ':
			result[i - 1] = result[i - 1][:-1]
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
	def enable_german_unicode():
		"""enable proper unicode punctuation"""
		ctx.settings["user.german_unicode"] = 1

	def disable_german_unicode():
		"""disable proper unicode punctuation"""
		ctx.settings["user.german_unicode"] = 0

	def smart_insert(txt: str):
		"""context-aware insertion"""

		# delete whatever is currently selected
		actions.key(" ")
		actions.key("backspace")

		with ClipScanner() as clip:

			# scan left side of the cursor
			clip.clear()
			actions.edit.extend_left()
			before = clip.get_selection()
			if before != "":
				actions.edit.extend_right()

			# scan right side of the cursor
			clip.clear()
			actions.edit.extend_right()
			after = clip.get_selection()
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

		if before in _capitalize_after or before == "":
			txt = txt[0].upper() + txt[1:]

		if settings.get("user.german_unicode") == 0:
			ascii = txt
			for c in _ascii_replace:
				ascii = ascii.replace(c, _ascii_replace[c])
			actions.insert(ascii)
		else:
			actions.insert(txt)

		if (
			after != ""
			and (
				txt[-1] in _space_after
				or unicodedata.category(txt[-1])[0] == 'L'
			)
			and after not in ' \n\t'
			and after not in _no_space_before
			and not squeeze_into_word
		):
			actions.insert(' ')

	def smart_delete(txt: str):
		"""delete word and optionally space"""

		with ClipScanner() as clip:

			for i in range(len(str(txt).split())):

				# first just delete all spaces until next word
				clip.clear()
				actions.edit.extend_word_left()
				before = clip.get_selection()
				if before != '' and before[-1] in [" ", "\n"]:
					actions.edit.extend_word_right()
					actions.key("backspace")
					continue

				# if there were none, delete next word
				actions.key("backspace")

				# delete spaces before that as well
				clip.clear()
				actions.edit.extend_left()
				before = clip.get_selection()
				if before in [" ", "\n"]:
					actions.key("backspace")
				elif before != '':
					actions.edit.extend_right()
