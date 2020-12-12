mode: user.german
-

^(englisch | english)$:
	mode.disable("user.german")
	mode.enable("command")

# "enter" is often confused with hinter/center/...
^eingabe$: key("enter")

^<user.weg>$: user.smart_delete(weg)

^speichern$: edit.save()

<user.satz>: user.smart_insert(satz)
