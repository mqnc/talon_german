mode: command
-

# note that when switching the engine, currently the switch command might be
# executed by both engines so it is important that both switch commands are
# defined for both engines and the one that shouldn't cause a switch just calls
# skip()

^german$:
	mode.disable("command")
	mode.enable("user.german")

english: skip()
