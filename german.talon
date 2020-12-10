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

# enter is often confused with hinter/center/...
^eingabe$: key("enter")

^<user.weg>$: user.smart_delete(weg)

^speichern$: edit.save()

<user.satz>: user.smart_insert(satz)
