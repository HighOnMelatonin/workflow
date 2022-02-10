##Combines project and team, to allow for an overview of various projects and teams
##Code has not be optimised (see overview.assignproject(), nested for loop)


import _team
import _project
import exceptions



class overview:
    def __init__(self, teams = list(), projects = list()) -> None:
        self.__teams = teams
        self.__projects = projects

    
    ##Project modifiers
    def addproject(self, title = str(), date = tuple((1, 1, 1)), teamic = str(), tasks = list()):
        self.__projects.append(_project.project(title, date, teamic, tasks))

    def removeproject(self, title):
        for i in range(len(self.__projects)):
            if self.__projects[i].gettitle() == title:
                self.__projects.pop(i)
                return

        raise exceptions.InvalidProjectName

    def allprojects(self):
        '''
        Returns a list of all the project objects
        '''
        return self.__projects

    def viewproject(self, title):
        '''
        Returns the details of 1 project
        '''
        for i in range(len(self.__projects)):
            if self.__projects[i].gettitle() == title:
                return self.__projects[i]

        raise exceptions.InvalidProjectName

    def addtask(self, title, taskname, date, desc):
        for i in range(len(self.__projects)):
            if self.__projects[i].gettitle() == title:
                self.__projects[i].addtask(taskname, date, desc)
                return

        raise exceptions.InvalidProjectName

    def removetask(self, title, taskname):
        removed = False
        for i in range(len(self.__projects)):
            if self.__projects[i].gettitle() == title:
                self.__projects.removetask(taskname)
                removed = True
                break

        if not removed:
            raise exceptions.InvalidProjectName

    def assignproject(self, teamic, title):
        assigned = False
        for i in range(len(self.__projects)):
            if self.__projects[i].gettitle() == title:
                teamfound = False
                for i in range(len(self.__teams)):
                    if self.__teams[i].getname() == teamic:
                        self.__teams[i].addproject(title)
                        teamfound = True
                        break
                
                if not teamfound:
                    raise exceptions.InvalidTeamName

                self.__projects[i].setteam(teamic)
                assigned = True
                break

        if not assigned:
            raise exceptions.InvalidProjectName



    ##team modifiers
    def addteam(self, teamname):
        this_team = _team.team()
        this_team.setname(teamname)
        self.__teams.append(this_team)
    
    def removeteam(self, teamname):
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].pop(i)
                return

        raise exceptions.InvalidTeamName

        

    def allteams(self):
        '''
        Returns a list of all the team objects
        '''
        return self.__teams

    def viewteam(self, teamname):
        '''
        Returns the details of 1 team
        '''
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                return self.__teams[i]

        raise exceptions.InvalidTeamName

    def _getteams(self):
        '''
        Returns a list of all team names
        '''
        teams = []
        for team in self.__teams:
            teams.append(team.getname())

        return teams

    def addmember(self, teamname, membername, position):
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].addmember(membername, position)
                return

        raise exceptions.InvalidTeamName

    def removemember(self, teamname, membername, position):
        removed = False
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].removemember(membername, position)
                removed = True
                break

        if not removed:
            raise exceptions.Ghost
        
        message = ''
        if self.__teams[i].getmembers() == []:
            self.__teams.pop(i)

            message = 'All members have been removed, team will be deleted automatically'

        return message

    
        




