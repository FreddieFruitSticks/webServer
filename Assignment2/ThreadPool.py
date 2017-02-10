from Queue import Queue
import threading, time

#Thread pool, polling the queue for tasks to run.
class ThreadPool (object):
	pool_size = 10
	pool = list()
	_queue = Queue()
	exit = False

	def __init__(self, pool_size):
		self.pool_size = pool_size

	def start(self):
		print 'start method'
		print self.pool_size
		for i in range(0,self.pool_size):
				self.pool.append(MyThread(target=self.poll_queue))
				print self.pool[i]
				self.pool[i].daemon = True
				self.pool[i].start()

	def poll_queue(self):
		while not self.exit:
			#use threading events rather. this is kak.
			if not self._queue.is_empty():
				print threading.current_thread(), "picked up queue"
				task = self._queue.pop()
				if task is not None:
					task_obj = task.value
					if task_obj is not None:
						print threading.current_thread(),' picked up task'
						task = task_obj.task
						kwargs = task_obj.kwargs
						task(kwargs.get('connection'), kwargs.get('file_name'))
			else:
				time.sleep(1)

	def close(self):
			self.exit=True

	def submit_task(self, task, kwargs):
		print kwargs
		task_obj = TaskObj(task, kwargs)
		self._queue.add(task_obj)

	def is_empty(self):
		return self._queue.is_empty()




class MyThread(threading.Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
		super(MyThread, self).__init__(group=group, target=target, name=name, kwargs=kwargs, verbose=verbose)




class TaskObj(object):
	task = None
	kwargs = None

	def __init__(self, task, kwargs):
		self.task = task
		self.kwargs = kwargs
