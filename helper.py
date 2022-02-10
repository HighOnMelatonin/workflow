##Combines project and team, to allow for an overview of various projects and teams
##Code has not be optimised (see overview.assignproject(), nested for loop)


import _team
import _project
import exceptions



class overview:
    '''
    Methods defined in the overview class
    
    overview.addproject(title, date, teamic, tasks)
    title: a string for the title of the project
    date: a tuple for the project's completion date, in the YYYY/MM/DD format
    teamic: a string for the name of the team in charge
    tasks: a list of tasks that need to be done for the project, each object in the list is an instance of a task

    overview.removeproject(title)
    title: name of the project to be removed


    '''
    def __init__(self, teams = list(), projects = list()) -> None:
        self.__teams = teams
        self.__projects = projects

    ##Private methods
    def _getproject(self, title):
        '''
        Returns the index of the project in the list of projects, raises
        InvalidProjectName error if project cannot be found
        '''
        for i in range(self.__projects):
            if self.__projects[i].gettitle() == title:
                return i

        raise exceptions.InvalidProjectName
    

    def _getteams(self):
        '''
        Returns a list of all team names
        '''
        teams = []
        for team in self.__teams:
            teams.append(team.getname())

        return teams


    def _getteam(self, teamname):
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                return i

        raise exceptions.GhostTeam



    ##Project modifiers
    def addproject(self, title = str(), date = tuple((1, 1, 1)), teamic = str(), tasks = list()):
        self.__projects.append(_project.project(title, date, teamic, tasks))

    def removeproject(self, title):
        i = self._getproject(title)
        self.__projects.pop(i)
        return

    def allprojects(self):
        '''
        Returns a list of all the project objects
        '''
        return self.__projects

    def viewproject(self, title):
        '''
        Returns the details of 1 project
        '''
        i = self._getproject(title)
        return self.__projects[i]

    def changeproname(self, title, newtitle):
        i = self._getproject(title)
        self.__projects[i].settitle(newtitle)


    def addtask(self, title, taskname, date, desc):
        i = self._getproject(title)
        self.__projects[i].addtask(taskname, date, desc)

    def removetask(self, title, taskname):
        i = self._getproject(title)
        self.__projects[i].removetask(taskname)

    def editdesc(self, title, taskname, newdesc):
        i = self._getproject(title)
        self.__projects[i].setdesc(taskname, newdesc)


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
                    raise exceptions.GhostTeam

                self.__projects[i].setteam(teamic)
                assigned = True
                break

        if not assigned:
            raise exceptions.InvalidProjectName


    def setprodue(self, title, date):
        ##date should be a tuple or list in the form YYYY/MM/DD
        i = self._getproject(title)
        self.__projects[i].setdue(date)


    def settaskdue(self, title, taskname, date):
        i = self._getproject(title)
        self.__projects[i].settaskdue(taskname, date)


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

        raise exceptions.GhostTeam

    def changename(self, teamname, newname):
        i = self._getteam(teamname)
        self.__teams[i].setname(newname)
        

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

        raise exceptions.GhostTeam

   
    def addmember(self, teamname, membername, position):
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].addmember(membername, position)
                return

        raise exceptions.GhostTeam

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

    
        




