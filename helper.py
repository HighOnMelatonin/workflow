'''
Combines project and team, to allow for an overview of various projects and teams to help the main program


Code has not be optimised (see overview.assignproject(), nested for loop)

'''

import _team
import _project
import exceptions



class overview:
    '''
    This class combines the project and team object, as one more layer of abstraction before being saved as a pkl file
    '''
    def __init__(self, teams = list(), projects = list()) -> None:
        self.__teams = teams
        self.__projects = projects

    ##Private methods
    def _getProject(self, title):
        '''
        Returns the index of the project in the list of projects, raises
        InvalidProjectName error if project cannot be found
        '''
        for i in range(len(self.__projects)):
            if self.__projects[i].gettitle() == title:
                return i

        raise exceptions.InvalidProjectName
    

    def _getTeams(self):
        '''
        Returns a list of all team names
        '''
        teams = []
        for team in self.__teams:
            teams.append(team.getname())

        return teams


    def _getTeam(self, teamname):
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                return i

        raise exceptions.GhostTeam


    def _checkDate(self, date):
        '''
        Checks if date is in the correct format (YYYY/MM/DD)
        Raises exceptions.InvalidDate if date is not in the right format
        DOES NOT CHECK IF THE DATE IS A VALID DATE, that is for datetime to do
        '''
        
        one, two, three = type(date[0]) == int, type(date[1]) == int, type(date[2]) == int
        if one and two and three:
            return

        else:
            raise exceptions.InvalidDate


    ##Project modifiers
    def addProject(self, title = str(), date = tuple((1, 1, 1)), teamic = str(), tasks = list()):
        '''
        Makes a new project

        :param title:   The title of the project
        :type title:    (str)

        :param date:    The project's completion date in YYYY/MM/DD format
        :type date:     tuple(int, int, int)

        :param teamic:  The team in charge of the project
        :type teamic:   (str)

        :param tasks:   Tasks to be done for the project
        :type tasks:    List[task]
        '''
        self._checkDate(date)
        self.__projects.append(_project.project(title, date, teamic, tasks))

    def removeProject(self, title):
        '''
        Deletes a project

        :param title:   Title of the project to be removed
        :type title:    (str)
        '''
        i = self._getProject(title)
        self.__projects.pop(i)
        return

    def allProjects(self):
        '''
        Returns a list of all the project objects

        :return: List[project]
        '''
        return self.__projects

    def viewProject(self, title):
        '''
        Returns the details of 1 project

        :param title:   The title of the project
        :type title:    (str)

        :return:        (project)
        '''
        i = self._getProject(title)
        return self.__projects[i]

    def changeProName(self, title, newtitle):
        '''
        Changes the project title

        :param title:       The original title of the project
        :type title:        (str)

        :param newtitle:    The new title of the project
        :type newtitle:     (str)
        '''
        i = self._getProject(title)
        self.__projects[i].settitle(newtitle)


    def addTask(self, title, taskname, date, desc):
        '''
        :param title:      Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be added
        :type taskname:     (str)

        :param date:        Due date for the task in YYYY/MM/DD format
        :type date:         tuple(int, int, int)

        :param desc:        Description of the task
        :type desc:         (str)
        '''
        self._checkDate()
        i = self._getProject(title)
        self.__projects[i].addtask(taskname, date, desc)

    def removeTask(self, title, taskname):
        '''
        :param title:      Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be removed
        :type taskname:     (str)
        '''
        i = self._getProject(title)
        self.__projects[i].removetask(taskname)

    def editDesc(self, title, taskname, newdesc):
        '''
        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be edited
        :type taskname:     (str)

        :param newdesc:     The new description to replace the previous
        :type newdesc:      (str)
        '''
        i = self._getProject(title)
        self.__projects[i].setdesc(taskname, newdesc)

    def taskDone(self, title, taskname):
        i = self._getProject(title)
        self.__projcts[i].taskDone(taskname)

    def taskUndone(self, title, taskname):
        p = self._getProject(title)
        self.__projects[p].taskUndone(taskname)


    def assignProject(self, teamic, title):
        '''
        :param teamic:  The name of the team in charge
        :type teamic:   (str)

        :param title:   The project title
        :type title:    (str)
        '''
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


    def setProDue(self, title, date):
        '''
        :param title:   Title of the project
        :type title:    (str)

        :param date:    New due date for the project, YYYY/MM/DD format
        :type date:     tuple(int, int, int)
        '''
        self._checkDate()
        i = self._getProject(title)
        self.__projects[i].setdue(date)


    def setTaskDue(self, title, taskname, date):
        '''
        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task
        :type taskname:     (str)

        :param date:        New due date for the task, YYYY/MM/DD format
        :type date:         tuple(int, int, int)
        '''
        self._checkDate()
        i = self._getProject(title)
        self.__projects[i].settaskdue(taskname, date)


    ##team modifiers
    def addTeam(self, teamname):
        '''
        :param teamname:    Name of the team
        :type teamname:     (str)
        '''
        this_team = _team.team()
        this_team.setname(teamname)
        self.__teams.append(this_team)
    
    def removeTeam(self, teamname):
        '''
        :param teamname:    Name of team to be removed
        :type teamname:     (str)
        '''
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].pop(i)
                return

        raise exceptions.GhostTeam

    def changeTeamName(self, teamname, newname):
        '''
        :param teamname:    Original team name
        :type teamname:     (str)

        :param newname:     New team name
        :type teamname:     (str)
        '''
        i = self._getTeam(teamname)
        self.__teams[i].setname(newname)
        

    def allTeams(self):
        '''
        Returns a list of all the team objects

        :return: List(team)
        '''
        return self.__teams

    def viewTeam(self, teamname):
        '''
        Returns the details of 1 team

        :return:    (team)
        '''
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                return self.__teams[i]

        raise exceptions.GhostTeam

   
    def addMember(self, teamname, membername, position):
        '''
        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the new member
        :type membername:   (str)

        :param position:    New member's position
        :type position:     (str)
        '''
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].addmember(membername, position)
                return

        raise exceptions.GhostTeam

    def removeMember(self, teamname, membername, position):
        '''
        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the member to be removed
        :type membername:   (str)

        :param position:    Position of the member
        :type postion:      (str)
        '''
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

    def changePos(self, teamname, membername, position, newpos):
        for i in range(len(self.__teams)):
            if self.__teams[i].getname() == teamname:
                self.__teams[i].changePos(membername, position, newpos)
                return

        raise exceptions.exceptions.GhostTeam






