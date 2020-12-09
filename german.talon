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
zirkumflex: auto_insert("^")

^eingabe$: key("enter")
^<user.weg>$: user.smart_delete(weg)
^speichern$: edit.save()

escape <user.text>:
	result = user.formatted_text(text, "ALL_LOWERCASE")
	auto_insert(result)
^(hoch | huch) <user.text>:
	result = user.formatted_text(text, "CAPITALIZE_FIRST_WORD")
	auto_insert(result)
(hoch | huch) <user.text>:
	result = user.formatted_text(text, "CAPITALIZE_FIRST_WORD")
	auto_insert(" " + result)
alles (hoch | huch) <user.text>:
	result = user.formatted_text(text, "ALL_CAPS")
	auto_insert(result)
<user.text>:
	result = user.formatted_text(text, "ALL_LOWERCASE")
	auto_insert(result)

alpha: auto_insert("a")
bravo: auto_insert("b")
charlie: auto_insert("c")
delta: auto_insert("d")
echo: auto_insert("e")
foxtrott: auto_insert("f")
golf: auto_insert("g")
hotel: auto_insert("h")
india: auto_insert("i")
julia: auto_insert(j"")
kilo: auto_insert("k")
lima: auto_insert("l")
mike: auto_insert("m")
november: auto_insert("n")
oskar: auto_insert("o")
papa: auto_insert("p")
québec: auto_insert("q")
romeo: auto_insert("r")
sierra: auto_insert("s")
tango: auto_insert("t")
uniform | uniformen: auto_insert("u")
viktor: auto_insert("v")
whisky: auto_insert("w")
x ray: auto_insert("x")
junkie: auto_insert("y")
zulu: auto_insert("z")
ärger: auto_insert("ä")
ökonom: auto_insert("ö")
übermut: auto_insert("ü")
s z: auto_insert("ß")
