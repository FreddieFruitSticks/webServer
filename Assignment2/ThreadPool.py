from Queue import Queue
import threading

class ThreadPool (object):
	pool_size = 10
	pool = []	
	_queue = Queue()
		
	def __init__(self, pool_size):
		self.pool_size = pool_size

	def start():
		thread_num = 0
		while True:
  	  if not self._queue.is_empty() and pool.length < pool_size:
				task_object = self._queue.pop().value
				pool[thread_num] = MyThread(target=task_object.task, kwargs=kwargs)
	
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

	
	
