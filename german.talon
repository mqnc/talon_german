mode: user.german
-

# note that when switching the engine, currently the switch command might be
# executed by both engines so it is important that both switch commands are
# defined for both engines and the one that shouldn't cause a switch just calls
# skip()

^(englisch | english)$:
	mode.disable("user.german")
	mode.enable("command")

german: skip()

# komma is often confused with komme
# enter is often confused with hinter/center/...
# groß often becomes große/großer/großes

leerzeichen | blank | blink | plenk | planck: auto_insert(" ")
punkt: auto_insert(". ")
pause: auto_insert(", ")
fragezeichen: auto_insert("? ")
ausrufezeichen: auto_insert("! ")
doppelpunkt: auto_insert(": ")
semikolon: auto_insert("; ")
bindestrich: auto_insert("-")
unterstrich: auto_insert("_")
schrägstrich: auto_insert("/")
backslash: auto_insert("\\")
senkrecht strich: auto_insert("|")
zitat: auto_insert('"')
apostroph: auto_insert("'")
klammer auf: auto_insert("(")
klammer zu: auto_insert(") ")
eckige klammer auf: auto_insert("[")
eckige klammer zu: auto_insert("] ")
geschweifte klammer auf: auto_insert("{")
geschweifte klammer zu: auto_insert("} ")
at | klammeraffe: auto_insert("@")
dollar: auto_insert("$")
und zeichen: auto_insert("&")
sternchen: auto_insert("*")
kleiner zeichen: auto_insert("<")
größer zeichen: auto_insert(">")
ist gleich zeichen: auto_insert("=")
raute: auto_insert("#")
tilde: auto_insert("~")
^eingabe$: key("enter")

escape <user.text>:
	result = user.formatted_text(text, "ALL_LOWERCASE")
	auto_insert(result)
(hoch | huch) <user.text>:
	result = user.formatted_text(text, "CAPITALIZE_FIRST_WORD")
	auto_insert(result)
alles (hoch | huch) <user.text>:
	result = user.formatted_text(text, "ALL_CAPS")
	auto_insert(result)
<user.text>:
	result = user.formatted_text(text, "ALL_LOWERCASE")
	auto_insert(result)
