'''
Handles the pkl files
'''

import os
import pickle
from typing import Any
import helper
import exceptions
import json


class handler:
    '''
    This class handles the pkl files that save all the instances and modifications made to the objects
    
    Modifications to the objects in the class do not reflect in the .pkl file immediately, user needs to commit before the changes are reflected in the file
    '''
    def __init__(self):
        '''
        Loads saved data from .pkl to self.master

        If required data files do not exist, the initialisation will create them
        '''
        if not os.path.isdir('misc'):
            os.mkdir('misc/')

        if not os.path.isdir('misc/projects'):
            os.mkdir('misc/projects/')
            if not os.path.isfile('misc/projects/projects.json'):
                self._makefile('misc/projects/projects.json')

        if not os.path.isdir('misc/teams'):
            os.mkdir('misc/teams/')
            if not os.path.isfile('misc/teams/teams.json'):
                self._makefile('misc/teams/teams.json')

        if not self._checkFile('misc/masterLog.pkl'):
            self._makefile('misc/masterLog.pkl')

            file = open('misc/masterLog.pkl','wb')
            self.master = helper.overview()
            pickle.dump(self.master, file)
            file.close()
        
        file = open('misc/masterLog.pkl','rb')
        try:
            self.master = pickle.load(file)
            print(self.master.allTeams())

        except:
            self.master = helper.overview()

        file.close()


    ##Private methods

    def _makefile(self, filename) -> None:
        '''
        Creates a new file with the filename specified

        :param filename:    The name of the file, including the file path
                            Example:
                            <filename> = 'misc/projects/Webstore project.pkl'
        :type filename:     (str)
        
        :return:            None
        '''
        newfile = open(filename, 'w')
        newfile.close()

    def _checkFile(self, filename, selectType = None) -> bool:
        '''
        _checkfile only checks if the file exists, it doesn't create a file, there is no return value file should be a .pkl file
        ! Only checks for project and team files !

        :param selectType:  Determines whether to raise invalid project or team error
        :type selectType:   (str)

        :param filename:    Name of the file to check, including the directory
        :type filename:     (str)

        :return:            (bool)
        '''
        if not os.path.isfile(filename):
            if selectType == 'p':
                print(exceptions.InvalidProjectName())

            elif selectType == 't':
                print(exceptions.GhostTeam())

            else:
                print(exceptions.InvalidType())
        
        else:
            return True

    def _saveFile(self, filename, data) -> None:
        '''
        Saves the new data to the file specified

        :param filename:    Name of the file, with .pkl extension
        :type filename:     (str)

        :param data:        The data to be dumped to the file
        :type data:         (team) or (project)

        :return:            None       
        '''

        try:
            output = open(filename, 'wb')
            pickle.dump(data, output)
            output.close()

        except:
            output = open(filename, 'x')
            output.close()


    def _getMaster(self):
        '''
        Return the master object

        :return:    handler.master
        '''
        return self.master


    def _getTeams(self) -> list:
        '''
        Get a list of all teams

        :return:    List
        '''
        raw = open('misc/teams/teams.json', 'r')
        output = json.load(raw)
        raw.close()
        return output

    def _addTeam(self, currTeam) -> None:
        '''
        Saves the team name of the new team to a json file

        :param currTeam:    The team object to be committed
        :type currTeam:     (team)

        :return:            None
        '''
        raw = open('misc/teams/teams.json', 'r+')
        output = json.load(raw)
        newteam = {'teamname':currTeam.getname()}
        output.append(newteam)
        raw.seek(0)
        json.dump(output, raw, indent = 4)
        raw.close()


    def _addProject(self, currProject) -> None:
        '''
        Saves the project title of the new project to a json file

        :param currProject: The project object to be committed
        :type currProject:  (project)

        :return:            None
        '''
        raw = open('mics/projects/projects.json', 'r+')
        output = json.load(raw)
        newproject = {'title':currProject.gettitle()}
        output.append(newproject)
        raw.seek(0)
        json.dump(output, raw, indent = 4)
        raw.close()
    
    def _getProjects(self) -> list:
        '''
        Return a list of all projects

        :return:    List
        '''
        raw = open('misc/projects/projects.json', 'r')
        output = json.load(raw)
        raw.close()
        return output



    ##Selecting
    def selectProject(self, projectname):
        '''
        Select an existing project to carry out modifications, so the user doesn't have to enter the project name repeatedly

        :param projectname: Name of the project
        :type projectname:  (str)

        :return:            (project)
        '''
        filename = 'misc/projects/' + projectname + '.json'
        self._checkfile(filename)
        super()._changeSelected(projectname, 'p')
        return self.master.viewProject(projectname)



    def selectTeam(self, teamname = str()):
        '''
        Select an existing team to carry out edits, so the user doesn't have to repeatedly enter the team name

        :param teamname:    Name of the team
        :type teamname:     (str)

        :return:            (team)
        '''

        filename = 'misc/teams/' + teamname + '.json'
        self._checkfile(filename)
        super()._changeSelected(teamname, 't')
        return self.master.viewTeam(teamname)

    

    ##Adding new
    ##Project
    def addProject(self, title = None, date = None, teamic = None, tasks = None) -> None:
        '''
        Creates a new project if the project does not exist, default date (if none is entered) is 0001/01/01
        If project exists, prompt the user to select the project instead

        :param title:       Title of the project
        :type title:        (str)

        :param date:        Date of completion in YYYY/MM/DD format
        :type date:         Tuple(int, int, int)

        :param teamic:      Team in charge of the project
        :type teamic:       (str)

        :param tasks:       Subtasks for the project
        :type tasks:        List(task)

        :return:            None
        '''
        filename = 'misc/projects/' + title + '.pkl'
        try:
            if self._checkFile(filename, 'p'):
                print(f"Project {title} already exists, to select it use the \"selectProject\" method instead")
                return

        except:
            if not date:
                date = [1, 1, 1]
            self.master.addProject(title, date, teamic, tasks)


    ##Task
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

        :return:            None
        '''
        filename = 'misc/projects/' + title + '.pkl'
        self._checkFile(filename)
        self.master.addTask(title, taskname, date, desc)
        


    ##Team
    def addTeam(self, teamname) -> None:
        '''
        Creates a new team if the team does not exist

        :param teamname:    The name of the team
        :type teamname:     (str)

        :return:            None
        '''
        filename = 'misc/teams/' + teamname + '.pkl'
        if self._checkFile(filename, 't'):
            print(f"Team {teamname} already exists, to select it use the \"selectTeam\" method instead")
            return

        self.master.addTeam(teamname)

    
    ##Member
    def addMember(self, teamname, name, position = None) -> None:
        '''
        Adds a new member to a specified team, raises exceptions.GhostTeam if team cannot be found
        
        :param teamname:    Name of the team
        :type teamname:     (str)

        :param name:        Name of the new member
        :type name:         (str)

        :param position:    New member's position
        :type position:     (str)

        :return:            None
        '''
        if not name:
            name = str(input("Name: "))
        
        if not position:
            position = str(input(f"{name}'s position: "))

        self.master.addMember(teamname, name, position)
    

    ##Modifying
    ##Project
    def changeProName(self, title, newtitle) -> None:
        '''
        Change the name of the project

        :param title:       Current title of the project
        :type title:        (str)

        :param newtitle:    New title for the project
        :type newtitle:     (str)

        :return:            None
        '''
        self.master.changeProName(title, newtitle)
    
    def setProdue(self, title, date) -> None:
        '''
        This method does not save the changes made to the instance in the pkl file yet
        Sets the completion date for the project

        :param title:   Project title
        :type title:    (str)

        :param date:    Project completion date, in YYYY/MM/DD format
        :type date:     Tuple(int, int, int)

        :return:        None
        '''
        self.master.setProDue(title, date)

    def assignProject(self, teamic, title) -> None:
        '''
        Assign the project to a team

        :param teamic:  The name of the team in charge
        :type teamic:   (str)

        :param title:   The project title
        :type title:    (str)

        :return:        None
        '''
        self.master.assignProject(teamic, title)

    def removeProject(self, title) -> None:
        '''
        Removes the specified project

        ;param title:   Title of the project to be removed
        :type title:    (str)

        :return:        None
        '''
        self.master.removeProject(title)


    ##Tasks
    def setTaskDue(self, title, taskname, date) -> None:
        '''
        Set the due date for a task
        Date format: YYYY/MM/DD

        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task
        :type taskname:     (str)

        :param date:        New due date for the task
        :type date:         Tuple(int, int, int)

        :return:            None
        '''
        self.master.setTaskDue(title, taskname, date)

    def removeTask(self, title, taskname) -> None:
        '''
        Removes the specified task

        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be removed
        :type taskname:     (str)

        :return:            None
        '''
        self.master.removeTask(title, taskname)

    def editDesc(self, title, taskname, newdesc) -> None:
        '''
        Edit the description of the specified task

        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task
        :type taskname:     (str)

        :param newdesc:     New description
        :type newdesc:      (str)

        :return:            None
        '''
        self.master.editDesc(title, taskname, newdesc)

    def taskDone(self, title, taskname) -> None:
        '''
        Mark task as done

        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            None
        '''
        self.master.taskDone(title, taskname)

    def taskUndone(self, title, taskname) -> None:
        '''
        Mark task as not done

        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            None
        '''
        self.master.taskUndone(title, taskname)
    
    ##Team
    def removeTeam(self, teamname) -> None:
        '''
        Removes the specified team

        :param teamname:    Name of the team to be removed
        :type teamname:     (str)

        :return:            None
        '''
        self.master.removeTeam(teamname)

    def changeTeamName(self, teamname, newname) -> None:
        '''
        Change the name of the specified team

        :param teamname:    Current team name
        :type teamname:     (str)

        :param newname:     New team name
        :type newname:      (str)

        :return:            None
        '''
        self.master.changeTeamName(teamname, newname)

    
    ##Member
    def removeMember(self, teamname, membername, position) -> None:
        '''
        Removes a member from the specified team

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the member to be removed
        :type membername:   (str)

        :param position:    Position of the member
        :type position:     (str)

        :return:            None
        '''
        self.master.removeMember(teamname, membername, position)

    def changePos(self, teamname, membername, position, newpos) -> None:
        '''
        Change the position of a member in the team

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param membername:  Name of the member
        :type membername:   (str)

        :param position:    The current position of the member
        :type position:     (str)
        
        :param newpos:      The new position for the member
        :type newpos:       (str)

        :return:            None
        '''
        self.master.changePos(self, teamname, membername, position, newpos)


    ##Display
    ##Projects
    def getProject(self, title):
        '''
        Returns the object with the specified title

        :param title:   Title of the project
        :type title:    (str)

        :return:    (project)
        '''
        return self.master.viewProject(title)

    def allProjects(self) -> list:
        '''
        Returns a list of all projects

        :return:    List(project)
        '''
        return self.master.allProjects()

    
    ##Tasks
    def getTask(self, title, taskname):
        '''
        Returns the details of a task

        :param title:       Title of the project
        :type title:        (str)

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            (task)
        '''
        p = self.master.viewProject(title)
        task = p.checktask(taskname)
        return task

    def allTasks(self, title) -> list:
        '''
        Returns a list of all tasks in the project specified

        :param title:   Project title
        :type title:    (str)

        :return:        List(task)
        '''
        p = self.master.viewProject(title)
        tasks = p.getTasks()
        return tasks


    ##Teams
    def getTeam(self, teamname):
        '''
        Returns the details of a team with the specified teamname

        :param teamname:    Name of the team
        :type teamname:     (str)

        :return:            (team)
        '''
        return self.master.viewTeam(teamname)

    def allTeams(self) -> list:
        '''
        Returns a list of all the teams

        :return:    List(team)
        '''
        print('here')
        return self.master.allTeams()

    
    ##Members
    def getMember(self, teamname, name, position):
        '''
        Return the details of a member

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param name:        Name of the member
        :type name:         (str)

        :param position:    Member's position
        :type position:     (str)

        :return:            (member)
        '''
        t = self.master.viewTeam(teamname)
        member = t.getMember(name, position)
        return member

    def allMembers(self) -> list:
        '''
        Returns a list of all members

        :return:    List(member)
        '''
        return self.master.allMembers()


    ##Commit
    def commit(self) -> None:
        '''
        Saves the changes made to the file
        
        :return:    None
        '''
        self._saveFile('misc/masterLog.pkl', self.master)



h = handler()
