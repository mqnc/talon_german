
import sys
import subprocess
import time
from talon import actions

USE_XCLIP = False
if (
	sys.platform.startswith('freebsd') or
	sys.platform.startswith('linux') or
	sys.platform.startswith('darwin')
):
	try:
		subprocess.run(['xclip', '-h'])
		USE_XCLIP = True
	except:
		print("installing xclip might make insertion way more snappy")
		print("sudo apt install xclip")

class ClipScanner:
	def __enter__(self):
		if USE_XCLIP:
			self.buffer = subprocess.check_output(['xclip', '-o'])
		self.clear()
		return self

	def __exit__(self, type, value, tb):
		if USE_XCLIP:
			with subprocess.Popen(['xclip', '-i'], stdin=subprocess.PIPE) as proc:
				proc.stdin.write(self.buffer)

	def get_selection(self):
		if USE_XCLIP:
			return subprocess.check_output(['xclip', '-o'], universal_newlines=True)
		else:
			return actions.edit.selected_text()

	def clear(self):
		if USE_XCLIP:
			subprocess.run(['xclip', '-i', '/dev/null'])
