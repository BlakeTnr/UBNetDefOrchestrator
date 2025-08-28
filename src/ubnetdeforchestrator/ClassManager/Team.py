from ubnetdeforchestrator.Person import Person

class Team:
    people: list[Person]
    
    def __init__(self):
        pass

    def addPerson(self, person: Person):
        self.people.append(person)