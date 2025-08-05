from abc import ABC, abstractmethod

class SysSecTeam(ABC):
    team_number: int

    def __init__(self, team_number: int):
        self.team_number = team_number
    
    @abstractmethod
    def setup(self):
        pass