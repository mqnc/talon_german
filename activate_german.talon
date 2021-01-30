mode: command
-
^german$:
	mode.disable("command")
	mode.enable("user.german")

^english$: skip()
