import numpy
from multiprocessing import shared_memory

class SMem:
    def __init__(self, name, size=1024, create=False):
        """
        Initializes a shared memory object.
        :param name: The name of the shared memory instance
        :param size: The size of the shared memory instance in bytes
        :param create: Whether to create a new shared memory instance
        """
        self.name = name
        self.size = size

        if create:
            self.shared_mem = shared_memory.SharedMemory(name=name, create=True, size=size)
        else:
            self.shared_mem = shared_memory.SharedMemory(name=name)

        self.buffer = numpy.ndarray((size,), dtype=numpy.uint8, buffer=self.shared_mem.buf)

    def write(self, data):
        """
        Writes data to the shared memory instance
        :param data: The data to write to the memory instance
        :return:
        """
        if len(data) > self.size:
            raise ValueError("Data size exceeds shared memory size")
        self.buffer[:len(data)] = numpy.frombuffer(data, dtype=numpy.uint8)
        self.buffer[len(data):] = 0

    def read(self) -> bytes:
        """
        Reads data from the shared memory instance
        :return: Returns the data read from the shared memory instance
        """
        end_idx = numpy.where(self.buffer == 0)[0][0]
        return self.buffer[:end_idx].tobytes()

    def close(self):
        """
        Detaches from the shared memory instance
        :return:
        """
        self.shared_mem.close()

    def unlink(self):
        """
        Unlinks the shared memory instance
        Only callable by the creator of the shared memory instance!
        :return:
        """
        self.shared_mem.unlink()