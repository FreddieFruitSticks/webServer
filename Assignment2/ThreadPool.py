from Queue import Queue
import threading, time


# Thread pool, polling the queue for tasks to run.
class ThreadPool(object):
    pool_size = 10
    _thread_queue = Queue()

    def __init__(self, pool_size):
        self.pool_size = pool_size

    def start(self):
        for i in range(0, self.pool_size):
            t = MyThread()
            self._thread_queue.add(t)

    def submit_task(self, task, kwargs):
        task_obj = TaskObj(task, kwargs)
        # thread = self._thread_queue.pop().value
        print task_obj.task
        thread = MyThread(target=task_obj.task, kwargs=task_obj.kwargs)
        # thread.set_target(task_obj.task, task_obj.kwargs)
        thread.start()

    def is_empty(self):
        return self._task_queue.is_empty()


class MyThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(MyThread, self).__init__(group=group, target=target, name=name, kwargs=kwargs, verbose=verbose)

    def run(self):
        super(MyThread, self).run()


# POPO
class TaskObj(object):
    task = None
    kwargs = None

    def __init__(self, task, kwargs):
        self.task = task
        self.kwargs = kwargs
