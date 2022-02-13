'''
the command line interface version



Workflow is a command line app that helps to streamline concurrent projects and task to various teams in an organisation
Should have an interface for admins and one for regular team members so that members from a different team cannot set a task as done for a project that wasn't assigned to them

'''

import helper
import json
import pickle
import exceptions
import os


class Running:
    '''
    This class handles the pkl files that save all the instances and modifications made to the objects
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
        
        file = open('misc/masterLog.pkl','wb')
        self.__master = pickle.load(file)
        self.__selected = str()
        file.close()


    ##Private methods
    def _changeSelected(self, new, selectType):
        '''
        Change the object selected, no checks are done in this method, checks should be done before accessing this method

        :param new:         The name of the new selection (project name or team name)
        :type new:          (str)

        :param selectType:  Determines whether the selection is a project or team
        :type selectType:   (str)

        :return:            The project or team object specified
        '''
        if selectType == 'p':
            self.__selected = self.__master.viewproject(new)
            return self.__selected

        elif selectType == 't':
            self.__selected = self.__master.viewteam(new)
            return self.__selected

        else:
            raise exceptions.InvalidType

    def _getselected(self):
        return self.__selected


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

    def _checkFile(self, filename, selectType):
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

    def _addteam(self, currTeam):
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


    def _addproject(self, currProject):
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
    
    def _getprojects(self):
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
        '''
        filename = 'misc/projects/' + projectname + '.json'
        self._checkfile(filename)
        super()._changeSelected(projectname, 'p')



    def selectTeam(self, teamname = str()):
        '''
        Select an existing team to carry out edits, so the user doesn't have to repeatedly enter the team name

        :param teamname:    Name of the team
        :type teamname:     (str)
        '''

        filename = 'misc/teams/' + teamname + '.json'
        self._checkfile(filename)
        super()._changeSelected(teamname, 't')

    

    ##Adding new
    ##Project
    def addproject(self, title = None, date = None, teamic = None, tasks = None):
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

        self.__master.addproject(title, date, teamic, tasks)
        self._saveFile(filename, self.__master._getproject(title))


    ##Task
    def addtask(self, title, taskname, date, desc):
        filename = 'misc/projects/' + title + '.pkl'
        self._checkFile(filename)
        


    ##Team
    def addteam(self, teamname):
        '''
        Creates a new team if the team does not exist

        :param teamname:    The name of the team
        :type teamname:     (str)
        '''
        filename = 'misc/teams/' + teamname + '.pkl'
        if self._checkFile(filename, 't'):
            print(f"Team {teamname} already exists, to select it use the \"selectTeam\" method instead")
            return

        self.__master.addteam(teamname)
        self._saveFile(filename, self.__master._getteam(teamname))

    
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
        self.__master.assignProject(teamic, title)

    def removeProject(self, title):
        self.__master.removeProject(title)

    ##Tasks
    def setTaskDue(self, title, taskname, date):
        self.__master.setTaskDue(title, taskname, date)





class interface():
    '''
    This class deals with the user interface
    '''
    def __init__(self):
        self.__background = Running()

    ##View
    ##Project
    def viewProject(self):
        pass