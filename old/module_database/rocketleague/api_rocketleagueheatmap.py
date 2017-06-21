import time
from threading import Thread, Event
from queue import Queue

from pyrope import Replay


def get_heatmap(replay_filename):
    replay = Replay(open(replay_filename))
    replay.parse_netstream()
    # status = Queue()
    # stop = Event()
    # thread = Thread(target=replay.parse_netstream, args=(status, stop))
    # thread.start()
    # while True:
    #     if status.empty():  # wait for status update
    #         time.sleep(0.1)
    #         continue
    #     i = status.get()
    #     if i == 'done':
    #         break
    #     elif i == 'exception':
    #         exc = status.get()
    #         raise exc
    #     elif i % 100 == 0:
    #         print(i)

if __name__ == '__main__':
    get_heatmap("837432FD4E763FC8AC4B3DB90AABD6C3.replay")
