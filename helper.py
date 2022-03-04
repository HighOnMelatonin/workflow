'''
Combines project and team, to allow for an overview of various projects and teams to help the main program


'''

import _team
import _project
import exceptions



class overview:
    '''
    This class combines the project and team object, as one more layer of abstraction before being saved as a pkl file
    '''
    def __init__(self, teams = list(), projects = list()) -> None:
        '''
        :param teams:       A list of all teams
        :type teams:        List(team)

        :param projects:    A list of all projects
        :type project:      List(project)
        '''
        self.__teams = teams
        self.__projects = projects

    ##Private methods
    def _getProject(self, title) -> int:
        '''
        Returns the index of the project in the list of projects, raises
        InvalidProjectName error if project cannot be found
        '''
        for i in range(len(self.__projects)):
            if self.__projects[i].getTitle() == title:
                return i

        raise exceptions.InvalidProjectName
    

    def _getTeams(self) -> list:
        '''
        Returns a list of all team names
        '''
        teams = []
        for team in self.__teams:
            teams.append(team.getName())

        return teams


    def _getTeam(self, teamname) -> int:
        '''
        Returns the index of the team in self.__teams
        If team cannot be found, raises exceptions.GhostTeam

        :param teamname:    Name of the team to find
        :type teamname:     (str)

        :return:            (int) or (exceptions.GhostTeam)
        '''
        for i in range(len(self.__teams)):
            if self.__teams[i].getName() == teamname:
                return i

        raise exceptions.GhostTeam


    def _checkDate(self, date) -> None:
        '''
        Checks if date is in the correct format (YYYY/MM/DD)
        Raises exceptions.InvalidDate if date is not in the right format
        DOES NOT CHECK IF THE DATE IS A VALID DATE, that is for datetime to do
        '''
        
        year, month, day = type(date[0]) == int, type(date[1]) == int, type(date[2]) == int
        if year and month and day:
            return

        else:
            raise exceptions.InvalidDate


    ##Project modifiers
    def addProject(self, title = str(), date = tuple((1, 1, 1)), teamic = str(), tasks = list()) -> None:
        '''
        Makes a new project

        :param title:   The title of the project
        :type title:    (str)

        :param date:    The project's completion date in YYYY/MM/DD format, default value is 1/1/1
        :type date:     tuple(int, int, int)

        :param teamic:  The team in charge of the project
        :type teamic:   (str)

        :param tasks:   Tasks to be done for the project
        :type tasks:    List[task]
        '''
        self._checkDate(date)
        self.__projects.append(_project.project(title, date, teamic, tasks))

    def removeProject(self, title) -> str:
        '''
        Deletes a project

        :param title:   Title of the project to be removed
        :type title:    (str)
        '''
        i = self._getProject(title)
        self.__projects.pop(i)
        return

    def allProjects(self) -> list:
        '''
        Returns a list of all the project objects

        :return: List(project)
        '''
        return self.__projects

    def viewProject(self, title):
        '''
        Returns the details of 1 project, a project object, if project cannot be found, raise exceptions.InvalidProjectName

        :param title:   The title of the project
        :type title:    (str)

        :return:        (project)
        '''
        i = self._getProject(title)
        return self.__projects[i]

    def changeProName(self, title, newtitle) -> None:
        '''
        Changes the project title

        :param title:       The original title of the project
        :type title:        (str)

        :param newtitle:    The new title of the project
        :type newtitle:     (str)
        '''
        i = self._getProject(title)
        self.__projects[i].setTitle(newtitle)


    def addTask(self, title, taskname, date, desc) -> None:
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
        self.__projects[i].addTask(taskname, date, desc)

    def removeTask(self, title, taskname) -> None:
        '''
        :param title:      Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be removed
        :type taskname:     (str)
        '''
        i = self._getProject(title)
        self.__projects[i].removeTask(taskname)

    def editDesc(self, title, taskname, newdesc) -> None:
        '''
        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be edited
        :type taskname:     (str)

        :param newdesc:     The new description to replace the previous
        :type newdesc:      (str)
        '''
        i = self._getProject(title)
        self.__projects[i].setDesc(taskname, newdesc)

    def taskDone(self, title, taskname) -> None:
        i = self._getProject(title)
        self.__projcts[i].taskDone(taskname)

    def taskUndone(self, title, taskname) -> None:
        p = self._getProject(title)
        self.__projects[p].taskUndone(taskname)


    def assignProject(self, teamic, title) -> None:
        '''
        Raises exceptions.InvalidProjectName or exceptions.GhostTeam if project or team, respectively, does not exist

        :param teamic:  The name of the team in charge
        :type teamic:   (str)

        :param title:   The project title
        :type title:    (str)
        '''
        i = self._getTeam(teamic)
        self.__teams[i].addProject(title)

        i = self._getProject(title)
        self.__projects[i].setTeam(teamic)

    def setProDue(self, title, date) -> None:
        '''
        :param title:   Title of the project
        :type title:    (str)

        :param date:    New due date for the project, YYYY/MM/DD format
        :type date:     tuple(int, int, int)
        '''
        self._checkDate()
        i = self._getProject(title)
        self.__projects[i].setDue(date)

    def setTaskDue(self, title, taskname, date) -> None:
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
        self.__projects[i].setTaskDue(taskname, date)


    ##team modifiers
    def addTeam(self, teamname) -> None:
        '''
        :param teamname:    Name of the team
        :type teamname:     (str)
        '''
        this_team = _team.team()
        this_team.setName(teamname)
        self.__teams.append(this_team)
    
    def removeTeam(self, teamname) -> None:
        '''
        If team cannot be found, raise exceptions.GhostTeam
        
        :param teamname:    Name of team to be removed
        :type teamname:     (str)
        '''
        i = self._getTeam(teamname)
        self.__teams.pop(i)

    def changeTeamName(self, teamname, newname) -> None:
        '''
        :param teamname:    Original team name
        :type teamname:     (str)

        :param newname:     New team name
        :type teamname:     (str)
        '''
        i = self._getTeam(teamname)
        self.__teams[i].setName(newname)
        

    def allTeams(self) -> list:
        '''
        Returns a list of all the team objects

        :return: List(team)
        '''
        return self.__teams

    def viewTeam(self, teamname):
        '''
        Returns the details of 1 team, if team cannot be found, raise exceptions.GhostTeam

        :return:    (team)
        '''
        for i in range(len(self.__teams)):
            if self.__teams[i].getName() == teamname:
                return self.__teams[i]

        raise exceptions.GhostTeam

   
    def addMember(self, teamname, membername, position) -> None:
        '''
        Add a new member to a specified team, raises exceptions.GhostTeam if specified team cannot be found

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the new member
        :type membername:   (str)

        :param position:    New member's position
        :type position:     (str)
        '''
        i = self._getTeam(teamname)
        self.__teams[i].addMember(membername, position)

    def removeMember(self, teamname, membername, position) -> str:
        '''
        If all members in the team have been removed, the team will automatically be removed as well

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the member to be removed
        :type membername:   (str)

        :param position:    Position of the member
        :type postion:      (str)
        '''

        i = self._getTeam(teamname)
        self.__teams[i].removeMember(membername, position)
        
        message = ''
        if self.__teams[i].getMembers() == []:
            self.__teams.pop(i)

            message = 'All members have been removed, team will be deleted automatically'

        return message

    def changePos(self, teamname, membername, position, newpos) -> None:
        '''
        Change the position of the specified member in the specified team, if team cannot be found, raise exceptions.GhostTeam.
        If member cannot be found, raise exceptions.Ghost

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the member
        :type membername:   (str)

        :param position:    Member's position, in the event that there are members with the same name
        :type position:     (str)

        :param newpos:      New position
        :type newpos:       (str)
        '''
        i = self._getTeam(teamname)
        self.__teams[i].changePos(membername, position, newpos)

    def allMembers(self) -> list:
        '''
        Returns a list of all the member objects

        :return: List(member)
        '''
        members = []
        for team in self.__teams:
            members += team.getMembers()

        return members





