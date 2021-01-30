mode: user.german
-

^(englisch | english)$:
	mode.disable("user.german")
	mode.enable("command")

^german: skip()

^unicode$:
	user.enable_german_unicode()

^kein unicode$:
	user.disable_german_unicode()

# "enter" is often confused with hinter/center/...
eingabe: key("enter")

# "weg" should only be recognized when it's not part of a sentence
# using token for counting the number of "weg"s
^<user.weg>$: user.smart_delete(weg)

^speichern$: edit.save()

<user.satz>: user.smart_insert(satz)
