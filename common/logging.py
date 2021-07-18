from logging import Formatter
from logging.handlers import BufferingHandler
from typing import List


class InMemoryHandler(BufferingHandler):
    def __init__(self, capacity: int, mask: str):
        BufferingHandler.__init__(self, capacity)
        self.formatter = Formatter(mask)

    def read(self) -> List[str]:
        self.acquire()
        try:
            return [self.formatter.format(record) for record in self.buffer]
        finally:
            self.release()
