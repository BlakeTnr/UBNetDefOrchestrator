from abc import ABC
from abc import abstractmethod
from syssec import Student
from syssec import Team

class Infra(ABC):
    @abstractmethod
    def createStudent(student: Student, password: str=None):
        pass

    @abstractmethod
    def createTeam(team: Team):
        pass

    @abstractmethod
    def assignStudentToTeam(student: Student, team: Team):
        pass