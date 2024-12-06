import numpy
from multiprocessing import shared_memory

class SMem:
    def __init__(self, name, size=1024, create=False):
        self.name = name
        self.size = size

        if create:
            self.shared_mem = shared_memory.SharedMemory(name=name, create=True, size=size)
        else:
            self.shared_mem = shared_memory.SharedMemory(name=name)

        self.buffer = numpy.ndarray((size,), dtype=numpy.uint8, buffer=self.shared_mem.buf)

    def write(self, data):
        if len(data) > self.size:
            raise ValueError("Data size exceeds shared memory size")
        self.buffer[:len(data)] = numpy.frombuffer(data, dtype=numpy.uint8)
        self.buffer[len(data):] = 0

    def read(self):
        end_idx = numpy.where(self.buffer == 0)[0][0]
        return self.buffer[:end_idx].tobytes()

    def close(self):
        self.shared_mem.close()

    def unlink(self):
        self.shared_mem.unlink()