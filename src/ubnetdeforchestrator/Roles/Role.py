from abc import ABC, abstractmethod

class Role(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def deploy():
        pass