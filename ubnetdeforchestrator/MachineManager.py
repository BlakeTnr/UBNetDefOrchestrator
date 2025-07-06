from abc import ABC, abstractmethod

class MachineManager(ABC):
    @abstractmethod
    def create_machine(self, name, cpu, memory, harddrive):
        """
        Create a virtual machine with the specified parameters.

        :param name: Name of the virtual machine.
        :param cpu: Number of CPU cores for the VM.
        :param memory: Amount of memory (RAM) for the VM in MB.
        :param harddrive: Size of the hard drive for the VM in GB.
        :return: ID of the created VM.
        """
        pass