from Queue import Queue
import threading
from ResponseBuilder import build_error_response


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
        try:
            thread = MyThread(target=task_obj.task, kwargs=task_obj.kwargs)
            # thread.set_target(task_obj.task, task_obj.kwargs)
            thread.start()
        except threading.ThreadError as e:
            conn = kwargs.get('connection', None)
            user_agent = kwargs.get('user_agent', None)
            if conn is not None:
                response_builder = build_error_response(500, "Internal server error", user_agent)
                conn.send(response_builder.build())
                print e
            else:
                raise e

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
