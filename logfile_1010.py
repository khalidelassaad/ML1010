class LogFile:
	def __init__(self, printfile):
		self.file = open(printfile, "w")
		return
	
	def print_to_file(self, string):
		self.file.write(string+"\n")
		return
	
	def close(self):
		self.file.close()
		return