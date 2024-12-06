import unittest
from smem.smem import SMem
import multiprocessing
import time


def writer_process():
    manager = SMem(name="ipc_memory", size=1024, create=True)
    try:
        manager.write(b"Message from writer process")
        time.sleep(5)
    finally:
        manager.close()
        manager.unlink()


def reader_process(results):
    time.sleep(1)
    manager = SMem(name="ipc_memory", create=False)
    try:
        results.append(manager.read())
    finally:
        manager.close()

class SMemTest(unittest.TestCase):

    def test_create_shared_memory(self):
        manager = SMem(name="test_memory", size=1024, create=True)
        try:
            self.assertEqual(manager.size, 1024)
            self.assertIsNotNone(manager.shared_mem)
        finally:
            manager.close()
            manager.unlink()

    def test_write_and_read(self):
        manager = SMem(name="test_memory", size=1024, create=True)
        try:
            message = b"Hello, shared memory!"
            manager.write(message)
            result = manager.read()
            self.assertEqual(message, result)
        finally:
            manager.close()
            manager.unlink()

    def test_write_overflow(self):
        manager = SMem(name="test_memory", size=16, create=True)
        try:
            large_data = b"This message is too long for the memory"
            with self.assertRaises(ValueError):
                manager.write(large_data)
        finally:
            manager.close()
            manager.unlink()

    def test_attach_to_existing_memory(self):
        creator = SMem(name="test_memory", size=1024, create=True)
        try:
            message = b"Data from creator"
            creator.write(message)

            reader = SMem(name="test_memory", size=1024, create=False)
            try:
                result = reader.read()
                self.assertEqual(message, result)
            finally:
                reader.close()
        finally:
            creator.close()
            creator.unlink()

    def test_interprocess_communication(self):
        results = multiprocessing.Manager().list()
        writer = multiprocessing.Process(target=writer_process)
        reader = multiprocessing.Process(target=reader_process, args=(results,))

        writer.start()
        reader.start()

        writer.join()
        reader.join()

        self.assertEqual(results[0], b"Message from writer process")

    def test_cleanup(self):
        manager = SMem(name="cleanup_test", size=1024, create=True)
        manager.close()
        manager.unlink()

        with self.assertRaises(FileNotFoundError):
            SMem(name="cleanup_test", create=False)

if __name__ == "__main__":
    unittest.main()