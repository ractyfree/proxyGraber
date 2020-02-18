
import threading

import time

class WorkerThreadPool():
	
	def __init__(self):
		self.pool = []

	def addThread(self, WorkerThread):
		self.pool.append(WorkerThread)

	def delThread(self, WorkerThread):
		self.pool.remove(WorkerThread)
	
	def isAllThreadsDone(self):
		while True:
			time.sleep(1)
			if all(x.is_alive() == False for x in self.pool):
				return
			continue



class WorkerThread(threading.Thread):
	def __init__(self, func, args):
		threading.Thread.__init__(self, name='Parsing')
		self.func = func
		self.args = args
		self._running = True
		self.start()


	def run(self):
		try:
			return self.func(self.args[0], self.args[1])
		except Exception as e:
			print('Thread error: {0}. Stacktrace: {1};{2};{3}'.format(e, self.func, self.args[0], self.args[1]))
			input()