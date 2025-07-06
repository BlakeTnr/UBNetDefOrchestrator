from abc import ABC, abstractmethod

from ubnetdeforchestrator.ProxmoxMachine import ProxmoxMachine

class ProxmoxLocation(ABC):
    @abstractmethod
    def add_machine(self, ProxmoxMachine: ProxmoxMachine):
        pass