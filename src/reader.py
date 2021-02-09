from threading import Event, Thread
import os
from os.path import isfile, join
from time import sleep
from sound import Audio, getaudio

buffer = []
BUFFER_SIZE = 100
END = '__end__'
CLOSED = False


def get_index(l, index, default):
    return l[index] if index < len(l) else default


class BufferFiller(Thread):
    global buffer, BUFFER_SIZE, END, CLOSED

    def __init__(self, event, fps, output_path):
        self.buffer_size = BUFFER_SIZE
        self.fps = fps

        _, _, files = next(os.walk(output_path))
        self.output_files = [
            f"{output_path}/{str(i+1)}.txt" for i in range(len(files))]

        Thread.__init__(self)
        self.stopped = event

    def is_buffer_full(self):
        return len(buffer) >= self.buffer_size

    def fill_buffer(self):
        if len(self.output_files) > 0:
            for _ in range(len(buffer), self.buffer_size):

                output_file = get_index(self.output_files, 0, END)
                if output_file == END:
                    self.close()
                    return

                with open(output_file) as f:
                    buffer.append(f.read())

                self.output_files.pop(0)
        else:
            self.close()

    def close(self):
        buffer.append(END)
        global CLOSED
        CLOSED = True
        self.stopped.set()
        return

    def run(self):
        while not self.stopped.wait(1/self.fps):
            if not self.is_buffer_full():
                self.fill_buffer()


def check_initializing():
    global CLOSED
    while(True):
        print(CLOSED)
        if (len(buffer) >= BUFFER_SIZE) or CLOSED:
            # buffer is full, can start video
            return
        print(f'initializing: {len(buffer)}%', end='\r')
        sleep(0.01)


def reader(fps, output_path):
    BufferFiller(Event(), fps, output_path).start()
    check_initializing()

    audio = Audio(join(output_path, "sound.mp3"))
    audio.start()
    while True:
        frame = get_index(buffer, 0, END)
        if frame == END:
            return
        print(frame)
        buffer.pop(0)
        sleep(1/(fps+2))
