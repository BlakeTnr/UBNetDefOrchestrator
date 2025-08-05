from abc import ABC, abstractmethod

class SysSecStudent(ABC):
    def __init__(self, identifier):
        self.identifier = identifier

    @abstractmethod
    def setup():
        pass