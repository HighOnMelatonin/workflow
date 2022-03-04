'''
Handles the pkl files
'''

import os
import pickle
import helper
import exceptions
import json


class handler:
    '''
    This class handles the pkl files that save all the instances and modifications made to the objects
    
    Modifications to the objects in the class do not reflect in the .pkl file immediately, user needs to commit before the changes are reflected in the file
    '''
    def __init__(self):
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
            self.__master = helper.overview()
            pickle.dump(self.__master, file)
            file.close()
        
        file = open('misc/masterLog.pkl','rb')
        try:
            self.__master = pickle.load(file)

        except:
            self.__master = helper.overview()

        file.close()


    ##Private methods

    def _makefile(self, filename):
        '''
        Creates a new file with the filename specified

        :param filename:    The name of the file, including the file path
        :type filename:     (str)

        Example:
        :filename:  misc/projects/Webstore project.pkl
        '''
        newfile = open(filename, 'w')
        newfile.close()

    def _checkFile(self, filename, selectType = None):
        '''
        _checkfile only checks if the file exists, it doesn't create a file, there is no return value file should be a .pkl file

        :param selectType:  Determines whether to raise invalid project or team error
        :type selectType:   (str)

        :param filename:    Name of the file to check, including the directory
        :type filename:     (str)
        '''
        if not os.path.isfile(filename):
            if selectType == 'p':
                raise exceptions.InvalidProjectName

            elif selectType == 't':
                raise exceptions.GhostTeam

            else:
                return False
        
        else:
            return True

    def _saveFile(self, filename, data):
        '''
        Saves the new data to the file specified

        :param filename:    Name of the file, with .pkl extension
        :type filename:     (str)

        :param data:        The data to be dumped to the file
        :type data:         (team) or (project)       
        '''
        output = open(filename, 'wb')
        pickle.dump(data, output)
        output.close()


    def _getMaster(self):
        return self.__master


    def _getTeams(self):
        raw = open('misc/teams/teams.json', 'r')
        output = json.load(raw)
        raw.close()
        return output

    def _addTeam(self, currTeam):
        '''
        Saves the team name of the new team to a json file

        :param currTeam:    The team object to be committed
        :type currTeam:     (team)
        '''
        raw = open('misc/teams/teams.json', 'r+')
        output = json.load(raw)
        newteam = {'teamname':currTeam.getname()}
        output.append(newteam)
        raw.seek(0)
        json.dump(output, raw, indent = 4)
        raw.close()

        ##Save the instance of the currTeam object
        filename = 'misc/teams/' + currTeam.getname() + '.pkl'
        newfile = open(filename, 'w')
        newfile.close()
        self._saveFile(filename, currTeam)


    def _addProject(self, currProject):
        '''
        Saves the project title of the new project to a json file

        :param currProject: The project object to be committed
        :type currProject:  (project)
        '''
        raw = open('mics/projects/projects.json', 'r+')
        output = json.load(raw)
        newproject = {'title':currProject.gettitle()}
        output.append(newproject)
        raw.seek(0)
        json.dump(output, raw, indent = 4)
        raw.close()
    
    def _getProjects(self):
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

        :return:            
        '''
        filename = 'misc/projects/' + projectname + '.json'
        self._checkfile(filename)
        super()._changeSelected(projectname, 'p')
        return self.__master.viewProject(projectname)



    def selectTeam(self, teamname = str()):
        '''
        Select an existing team to carry out edits, so the user doesn't have to repeatedly enter the team name

        :param teamname:    Name of the team
        :type teamname:     (str)
        '''

        filename = 'misc/teams/' + teamname + '.json'
        self._checkfile(filename)
        super()._changeSelected(teamname, 't')
        return self.__master.viewTeam(teamname)

    

    ##Adding new
    ##Project
    def addProject(self, title = None, date = None, teamic = None, tasks = None):
        '''
        Creates a new project if the project does not exist

        :param title:       Title of the project
        :type title:        (str)

        :param date:        Date of completion in YYYY/MM/DD format
        :type date:         Tuple(int, int, int)

        :param teamic:      Team in charge of the project
        :type teamic:       (str)

        :param tasks:       Subtasks for the project
        :type tasks:        List(task)
        '''
        filename = 'misc/project/' + title + '.pkl'
        if self._checkfile(filename, 'p'):
            print(f"Project {title} already exists, to select it use the \"selectProject\" method instead")
            return

        self.__master.addProject(title, date, teamic, tasks)
        self._saveFile(filename, self.__master._getproject(title))


    ##Task
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
        filename = 'misc/projects/' + title + '.pkl'
        self._checkFile(filename)
        self.__master.addTask(title, taskname, date, desc)
        


    ##Team
    def addTeam(self, teamname):
        '''
        Creates a new team if the team does not exist

        :param teamname:    The name of the team
        :type teamname:     (str)
        '''
        filename = 'misc/teams/' + teamname + '.pkl'
        if self._checkFile(filename, 't'):
            print(f"Team {teamname} already exists, to select it use the \"selectTeam\" method instead")
            return

        self.__master.addTeam(teamname)
        self._saveFile(filename, self.__master._getteam(teamname))

    
    ##Member
    def addMember(self, teamname, name, postion):
        '''
        :param teamname:    Name of the team
        :type teamname:     (str)

        :param name:        Name of the new member
        :type name:         (str)

        :param position:    New member's position
        :type position:     (str)
        '''
        self.__master.addMember(teamname, name, postion)
    

    ##Modifying
    ##Project
    def changeProName(self, title, newtitle):
        self.__master.changeProName(title, newtitle)
    
    def setProdue(self, title, date):
        '''
        This method does not save the changes made to the instance in the pkl file yet

        :param title:   Project title
        :type title:    (str)

        :param date:    Project completion date, in YYYY/MM/DD format
        :type date:     Tuple(int, int, int)
        '''
        self.__master.setProDue(title, date)

    def assignProject(self, teamic, title):
        '''
        :param teamic:  The name of the team in charge
        :type teamic:   (str)

        :param title:   The project title
        :type title
        '''
        self.__master.assignProject(teamic, title)

    def removeProject(self, title):
        self.__master.removeProject(title)


    ##Tasks
    def setTaskDue(self, title, taskname, date):
        self.__master.setTaskDue(title, taskname, date)

    def removeTask(self, title, taskname):
        self.__master.removeTask(title, taskname)

    def editDesc(self, title, taskname, newdesc):
        self.__master.editDesc(title, taskname, newdesc)

    def taskDone(self, title, taskname):
        self.__master.taskDone(title, taskname)

    def taskUndone(self, title, taskname):
        self.__master.taskUndone(title, taskname)
    
    ##Team
    def removeTeam(self, teamname):
        self.__master.removeTeam(teamname)

    def changeTeamName(self, teamname, newname):
        self.__master.changeTeamName(teamname, newname)

    
    ##Member
    def removeMember(self, teamname, membername, position):
        self.__master.removeMember(teamname, membername, position)

    def changePos(self, teamname, membername, position, newpos):
        self.__master.changePos(self, teamname, membername, position, newpos)


    ##Display
    ##Projects
    def getProject(self, title):
        '''
        :return:    (project)
        '''
        return self.__master.viewProject(title)

    def allProjects(self):
        return self.__master.allProjects()

    
    ##Tasks
    def getTask(self, title, taskname):
        p = self.__master.viewProject(title)
        task = p.checktask(taskname)
        return task

    def allTasks(self, title):
        p = self.__master.viewProject(title)
        tasks = p.gettasks()
        return tasks


    ##Teams
    def getTeam(self, teamname):
        return self.__master.viewTeam(teamname)

    def allTeams(self):
        return self.__master.allTeams()

    
    ##Members
    def getMember(self, teamname, name, position):
        t = self.__master.viewTeam(teamname)
        member = t.getMember(name, position)
        return member

    def allMembers(self, teamname):
        t = self.__master.allTeams()
        members = t.getmembers
        return members

    

    ##Commit
    def commit(self):
        '''
        Saves the changes made to the file
        '''
        self._saveFile('misc/masterLog.pkl', self.__master)

