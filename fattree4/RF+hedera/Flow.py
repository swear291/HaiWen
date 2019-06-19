class Flow:
	def __init__(self, start_time, src, dst):
		self.start_time = start_time
		self.src = src
		self.dst = dst
	def printFlow(self):
		print 'from ' + str(self.src) + ' to ' + str(self.dst)

if __name__ == '__main__':
	flow = Flow(1,2,3)
	print flow.src
	flow.printFlow()