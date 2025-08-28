from ubnetdeforchestrator.ClassManager.Team import Team

def Class():

    def __init__(self):
        self.teams = []
        pass

    def addTeam(self, team: Team):
        self.teams.append(team)