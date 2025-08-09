from abc import ABC
from abc import abstractmethod
from syssec import Student
from syssec import Team

class Infra(ABC):
    @abstractmethod
    def createStudent(student: Student):
        pass

    @abstractmethod
    def createTeam(team: Team):
        pass
