import abc
from ubnetdeforchestrator.Roles.Role import Role
from ubnetdeforchestrator.Person import Person

allAssignments: list = []

class PersonRoleAssignment():
    def __init__(self, person: Person, role: Role):
        self.person = person
        self.role = role
        allAssignments.append(self)