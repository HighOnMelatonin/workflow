'''
the command line interface version

Workflow is a command line app that helps to streamline concurrent projects and task to various teams in an organisation

**Assumes task names do not contain any spaces
**Assumes team members' names do not contain any spaces
'''

import exceptions
import sqlite3
import _team
import _project
import os
from getpass import getpass
from handler import handler


class interface:
    '''
    This class deals with the user interface

    self.__active is the project or teamname that is currently being modified
    self.background is everthing else, all the other projects and teams

    separating self.__active from self.background so that the user can modify the same project or team without having to repeatedly input the team/project name
    '''
    def __init__(self):
        self.background = handler()
        self.__active = None


    ##Active
    def _changeActive(self, new, datatype) -> None:
        '''
        Changes the value of self.__active to the object selected, if nothing is selected, raise exceptions.InvalidType

        :param new:         The title of the project or team name
        :type new:          (str)

        :param datatype:    Determines whether its a project or team
        :type datatype:     (str)

        :return:            None
        '''
        if datatype == 'p' or datatype == 'project':
            self.__active = self.background.getProject(new)

        elif datatype == 't' or datatype == 'team':
            self.__active = self.background.getTeam(new)

        else:
            raise exceptions.InvalidType

    def _getActive(self):
        '''
        Returns the currently selected object, either a (project) or a (team)

        :return:    (project) or (team)
        '''
        return self.__active


    ##Get input
    def _getDate(self) -> tuple:
        '''
        Gets user input for a date in the format "YYYY/MM/DD" and returns the date as a tuple in the format (YYYY,MM,DD)

        :return:    Tuple(int, int, int)
        '''
        date = str(input("Date (YYYY/MM/DD): "))

        date = date.split('/')

        for i in range(len(date)):
            date[i] = int(date[i])

        return tuple(date)

    def _getTask(self) -> str:
        '''
        Shows a list of all the tasks to get user input and returns user's choice

        :return:    (str)
        '''
        tasks = self.background.allTasks()
        print(tasks)
        taskname = str(input("Task name: "))
        return taskname


    ##Selection
    def selection(self, datatype = None, name = None) -> None:
        '''
        Change the active object being modified, raises exception.InvalidType if the object is neither a (team) nor (project)
        If datatype is not specified, get user input for the datatype
        If name is not specified, get user input for the name of the team or the project title

        interface._changeActive() already catches invalid names, so there is no need to check again here


        :param datatype:    Selection of a project or a team
        :type datatype:     (str)

        :param name:        Project title or team name
        :type name:         (str)

        :return:            None
        '''
        if not datatype:
            datatype = str(input("Do you want to modify a project or a team?\n"))

        if datatype == 'project' and not name:
            projects = self.background.allProjects()
            print("List of projects: ")
            for project in projects:
                print(project.getTitle())

            name = str(input("Selection: "))

        elif datatype == 'team' and not name:
            teams = self.background.allTeams()
            print("List of teams: ")
            for team in teams:
                print(team.getName())

            team = str(input("Selection: "))

        else:
            raise exceptions.InvalidType

        self._changeActive(name, datatype)


    ##View
    def view(self) -> None:
        '''
        Displays details of a project or a team, depending on what has been selected
        Raises exceptions.MethodMadness if no object is selected

        :return:    None
        '''
        if type(self.__active) == _project.project:
            project = self.background.getProject(self.__active.getTitle())
            project.display()

        elif type(self.__active) == _team.team:
            team = self.background.getTeam(self.__active.getName())
            team.display()

        else:
            raise exceptions.MethodMadness(exceptions.WrongSelection)


    def viewAll(self) -> None:
        '''
        View all projects or teams, raises exceptions.InvalidType if no object is selected

        :return:    None
        '''
        if type(self.__active) == _team.team:
            teams = self.background.allTeams()
            for team in teams:
                team.display()

        elif type(self.__active) == _project.project:
            projects = self.background.allProjects()
            for project in projects:
                project.display()

        else:
            raise exceptions.InvalidType


    ##Project
    def projectStatus(self) -> None:
        '''
        Prints the project status in percentage form
        If selected object is not a (project), raise exceptions.MethodMadness

        :return:    None
        '''
        if type(self.__active) == _project.project:
            status = self.__active.getStatus()
            print(f"{self.__active.getTitle()} is {status*100:.2f}% complete")

        else:
            print(exceptions.MethodMadness())

    def getTitle(self) -> str:
        '''
        Return project title for the selected project
        If selected object is not a (project), raise exceptions.MethodMadness

        :return:    (str)
        '''
        if self.getType() == 'p':
            return self.__active.getTitle()

        else:
            print(exceptions.MethodMadness())


    ##Team
    def getName(self) -> str:
        '''
        Return team name for the selected team
        If selected object is not a (team), raise exceptions.MethodMadness

        :return:    (str)
        '''
        if self.getType() == 't':
            return self.__active.getName()

        else:
            print(exceptions.MethodMadness())


    ##Member
    def viewMembers(self) -> None:
        '''
        View all members (without team names)
        Prints the names and position of all members

        :return:    None
        '''
        if type(self.__active) == _project.project:
            raise exceptions.InvalidType

        else:
            members = self.background.allMembers()
            print(f"{'Name':<30}{'Position':>20}")
            for member in members:
                print(f"{member.getName():<30}{member.getPosition():>20}")


    ##Editing
    #Tasks
    def taskDone(self, taskname) -> None:
        '''
        Marks a task as done

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            None
        '''
        self.__active.checkTask(taskname)


    ##Get type
    def getType(self) -> str:
        '''
        Returns the type of object currently selected, a team ('t') or a project ('p'). If none is selected, raises exceptions.InvalidType

        :return:    (str)
        '''
        if type(self.__active) == _project.project:
            return 'p'

        elif type(self.__active) == _team.team:
            return 't'

        else:
            raise exceptions.InvalidType

    ##Commit
    def commit(self) -> None:
        '''
        Saves the changes made to the objects to a .pkl file

        :return:    None
        '''
        self.background.commit()



class admin(interface):
    '''
    This class deals with the user interface for admins, making more methods available
    '''
    def __init__(self):
        super().__init__()
        if not os.path.isfile('misc/data/admins.db'):
            ##If admin database does not exist, create it and add the default admin
            ##with name "admin" and default password "a1b2c3d4e5"
            ##For security, please delete the default admin
            newdb = open("misc/data/admins.db", 'x')
            newdb.close()

            db = sqlite3.connect('misc/data/admins.db')
            password = self._encode('a1b2c3d4e5')
            db.execute('INSERT INTO ACCOUNTS VALUES(?,?)', ('admin',password))
            


    ##Private methods
    def _checkAdmin(self, name, password) -> bool:
        '''
        :param name:        Registered admin name
        :type name:         (str)

        :param password:    Password for the corresponding admin, password passed into this method must be encoded first
        :type password:     (str)

        :return:            (bool)
        '''
        db = sqlite3.connect('misc/data/admins.db')
        cursor = db.execute("SELECT * FROM ACCOUNTS")
        allAdmin = cursor.fetchall()
        if (name, password) in allAdmin:
            return True

        else:
            return False

    def _addAdmin(self, name, password) -> None:
        '''
        Adds a new admin to the database, password is case-sensitve
        No repetition of names allowed as the name is the primary key
        
        :param name:        Admin name to be registered
        :type name:         (str)

        :param password:    Password for the corresponding admin, password should not be encoded
        :type password:     (str)

        :return:            None
        '''
        db = sqlite3.connect('misc/data/admins.db')
        cursor = db.execute('SELECT * FROM ACCOUNTS')
        password = self._encode(password)
        for account in cursor:
            if account[0] == name:
                if self._checkAdmin(name, password):
                    print("Admin account with the same name exists, attempting to sign you in...")
                    return self._checkAdmin(name, password)

                else:
                    raise exceptions.Clone

        db.execute('INSERT INTO ACCOUNTS VALUES(?,?)',(name, password))
        db.commit()
        print("New account added")


    def _encode(self, password) -> str:
        '''
        Takes a string as parameter and returns the encoded version of the string

        :param password:    The password as a raw string
        :type password:     (str)

        :return:            (str)
        '''
        encoded = ''
        for char in password:
            newchar = str(ord(char))
            encoded += newchar.ljust(3, '0')

        return encoded

    def _decode(self, encoded) -> str:
        '''
        Takes an encoded string as parameter and returns the decoded version

        :param encoded: The encoded password
        :type encoded:  (str)

        :return:        (str)
        '''
        password = ''
        for i in range(len(encoded), step = 3):
            char = chr(int(encoded[i: i + 3]))
            password += char

        return password


    ##Validate admin
    def validate(self) -> bool:
        '''
        Checks if the user is an admin, takes name and password input from user

        :return:    (bool)
        '''
        name = str(input("Name: "))
        password = getpass('Password (hidden): ')

        return self._checkAdmin(name, self._encode(password))


    ##Add new
    ##Project
    def addProject(self, title = None, date = None, teamic = None, tasks = []) -> None:
        '''
        Creates a new project, param title must be filled
        If title is not filled, this method will prompt the user for an input

        :param title:   Project title
        :type title:    (str)

        :param date:    Date of completion
        :type date:     Tuple(int, int, int)

        :param teamic:  Team in charge of the project
        :type teamic:   (str)

        :param tasks:   Subtasks to be completed for the project
        :type tasks:    list(task)

        :return:        None
        '''
        if not title:
            title = str(input("Project title: "))
        
        self.background.addProject(title, date, teamic, tasks)


    ##Admin
    def addAdmin(self) -> None:
        '''
        Only an admin can add a new admin
        Gets user input for name and password, prompting the user to input the password twice to reduce errors
        If passwords do not match, get the user to re-enter everything

        :return:    None
        '''
        name = str(input("Name (for logging in): "))
        pass1 = getpass('Password (hidden): ')
        pass2 = getpass('Re-enter password (hidden): ')

        if pass1 != pass2:
            self.addAdmin()

        else:
            self._addAdmin(name, pass1)

    
    ##Team
    def addTeam(self, teamname = None, members = []) -> None:
        '''
        Makes a new team, if teamname is not specified, gets user input for team name
        Adds every member specified to the team

        :param teamname:    Name of the team
        :type teamname:     (str)

        :param members:     Names of the members in the team
        :type members:      List(str)

        :return:            None
        '''
        if not teamname:
            teamname = str(input("Team name: "))

        self.background.addTeam(teamname)

        for member in members:
            self.background.addMember(teamname, member, None)


    ##Task
    def addTask(self, title = None, taskname = None, date = None, desc = None) -> None:
        '''
        Add a new task to the project, if any parameter is not filled, prompt the user to input, except for description
        If selected object is not a (project), raise exception.WrongSelection

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
        if self.getType() == 'p':
            if not title:
                title = str(input("Project title: "))

            if not taskname:
                taskname = str(input("Task name: "))

            if not date:
                date = self._getDate()

            self.background.addTask(self.__active.getTitle(), taskname, tuple(date), desc)

        else:
            print(exceptions.WrongSelection())


    ##Member
    def addMember(self, name = None, position = None) -> None:
        '''
        Adds a new member to the selected team, if any parameter is not specified, prompt the user
        If selected object is not a (team), raise exceptions.WrongSelection()

        :param name:        Name of the new member
        :type name:         (str)

        :param position:    New member's position
        :type position:     (str)

        :return:            None
        '''
        if self.getType() == 't':
            if not name:
                name = str(input("Name: "))

            if not position:
                position = str((input("Position: ")))
        
            self.background.addMember(self.__active.getName(), name, position)

        else:
            print(exceptions.WrongSelection())


    ##Modifications
    ##Project
    def changeProName(self, newtitle = None) -> None:
        '''
        Changes the name of the project, if the new title is not specified, prompt the user
        If selected object is not a (project), raise exceptions.WrongSelection

        :param newtitle:    New project title
        :type newtitle:     (str)

        :return:            None
        '''
        if self.getType() == 'p':
            if not newtitle:
                newtitle = str(input("New title: "))

            self.background.changeProName(self.__active.getTitle(), newtitle)

        else:
            print(exceptions.WrongSelection())

    def changeProDue(self, date = None) -> None:
        '''
        Changes the completion date for the project, if new date is not specified, prompt the user
        If selected object is not a (project), raise exceptions.WrongSelection

        :param date:    Project completion date, in YYYY/MM/DD/ format
        :type date:     Tuple(int, int, int)

        :return:        None
        '''
        if self.getType() == 'p':
            if not date:
                date = self._getDate()

            else:
                date = date.split('/')

                for i in range(len(date)):
                    date[i] = int(date[i])

            self.background.setProdue(self.__active.getTitle(), tuple(date))

        else:
            print(exceptions.WrongSelection())

    def assignProject(self, teamic = None) -> None:
        '''
        Assigns the project to a team, if team in charge is not specified, prompt the user
        If selected object is not a (project), raise exceptions.WrongSelection

        :param teamic:  The name of the team in charge
        :type teamic:   (str)

        :return:        None
        '''
        if self.getType() == 'p':
            if not teamic:
                teams = self.background.allTeams()
                print(teams)
                teamic = str(input("Team in-charge: "))

            self.background.assignProject(teamic, self.__active.getTitle())

        else:
            print(exceptions.WrongSelection())

    def removeProject(self) -> None:
        '''
        Removes the current project
        If selected object is not a (project), raise exceptions.WrongSelection

        :return:    None
        '''
        if self.getType() == 'p':
            self.background.removeProject(self.__active.getTitle())

        else:
            print(exceptions.WrongSelection())


    ##Tasks
    def setTaskDue(self, taskname = None, date = None) -> None:
        '''
        Changes the due date of a task, if task name and new date is not specified, prompt user
        If selected object is not a (project), raise exception.WrongSelection

        :param taskname:    The name of the task
        :type taskname:     (str)

        :param date:        The new due date in the format "YYYY/MM/DD"
        :type date:         (str)

        :return:            None
        '''
        if self.getType() == 'p':
            if not taskname:
                taskname = self._getTask()

            if not date:
                date = self._getDate()

            else:
                date = date.split('/')

                for i in range(len(date)):
                    date[i] = int(date[i])
            
            self.background.setTaskDue(self.__active.getTitle(), taskname, date)

        else:
            print(exceptions.WrongSelection())
    
    def removeTask(self, taskname) -> None:
        '''
        Removes the specified task from the selected project
        If selected object is not a (project) raise exceptions.WrongSelection

        :param taskname:    The name of the task to be removed
        :type taskname:     (str)

        :return:            None
        '''
        if self.getType() == 'p':
            if not taskname:
                taskname = self._getTask()

            self.background.removeTask(self.__active.getTitle(), taskname)

        else:
            print(exceptions.WrongSelection())

    def editDesc(self, taskname = None, newdesc = None) -> None:
        '''
        Edit the description of a task from the selected project
        If the selected object is not a (project), raise exception.WrongSelection
        If any parameters are not specified, prompt user

        :param taskname:    The name of the task
        :type taskname:     (str)

        :param newdesc:     The new description of the task
        :type newdesc:      (str)

        :return:            None
        '''
        if self.getType() == 'p':
            if not taskname:
                taskname = self._getTask()

            if not newdesc:
                newdesc = str(input("New description: "))

            self.background.editDesc(self.__active.getTitle(), taskname, newdesc)

        else:
            print(exceptions.WrongSelection())


    ##Teams
    def removeTeam(self) -> None:
        '''
        Removes the selected team
        If selected object is not a team, raise exception.WrongSelection

        :return:    None
        '''
        if self.getType() == 't':
            self.background.removeTeam(self.__active.getName())

        else:
            print(exceptions.WrongSelection())

    def changeTeamName(self, newname = None) -> None:
        '''
        Change the name of the selected team, if the selected object is not a (team), raise exception.WrongSelection
        If newname is not specified, prompt the user

        :param newname: The new team name
        :type newname:  (str)

        :return:        None
        '''
        if self.getType() == 't':
            if not newname:
                newname = str(input("New team name: "))

            self.background.changeTeamName(self.__active.getName(), newname)
        
        else:
            print(exceptions.WrongSelection())


    ##Member
    def removeMember(self, membername, position) -> None:
        '''
        Removes a member from the team, if any parameter is not filled, prompt the user
        If the selected object is not a (team), raise exceptions.WrongSelection

        :param membername:  Name of the member to be removed
        :type membername:   (str)

        :param position:    Member's position, in case there are members in the team with the same name
        :type position:     (str)

        :return:            None
        '''
        if self.getType() == 't':
            if not membername:
                membername = str(input("Member name: "))

            if not position:
                position = str(input("Member's position: "))

            self.background.removeMember(self.__active.getName(), membername, position)

        else:
            print(exceptions.WrongSelection())

    def changePos(self, membername, position, newpos) -> None:
        '''
        Change the position of a specified member
        If any parameter is not filled, prompt the user
        If the selected object is not a (team), raise exceptions.WrongSelection

        :param membername:  Name of the member
        :type membername:   (str)

        :param position:    Member's position
        :type position:     (str)

        :param newpos:      New position
        :type newpos:       (str)

        :return:            None
        '''
        if self.getType() == 't':
            if not membername:
                membername = str(input("Member name: "))

            if not position:
                position = str(input("Member's position: "))

            if not newpos:
                newpos = str(input("Member's new position: "))

            self.background.changePos(self.__active.getName, membername, position, newpos)

        else:
            print(exceptions.WrongSelection())


    ##Help message
    def getHelp(self) -> str:
        '''
        Returns the help message for admins

        :return:    (str)
        '''
        mainMessage = """
        WorkFlow terminal
        The command line app that helps streamline your workflow
        
        Commands:
        help        Returns this message when executed

        commit      Saves changes made to the files

        exit        Exits the program without saving changes

        login       Login to your admin account for privileges

        select      Select a project or team to view or modify
                    > select <"project"/"team"> <project title/team name>

        view        View the details of the selected project or team

        viewAll     View all projects or teams, if a team is selected, details of all the teams will be shown, if a project is selected, details of all the projects will be shown

        status      Show project status

        title       Returns the project title

        name        Returns the team name

        members     Shows the details of all members in the selected team

        done        Marks a task as done
                    > done <taskname>

        undone      Marks a task as not done
                    > undone <taskname>



        Admin commands:
        addAdmin        Adds a new admin to the database, only existing admins can add new admins
                        (Admin)> addAdmin

        addMember       Adds a new member to the team selected
                        (Admin)> addMember <name> <position>

        addProject      Creates a new project
                        (Admin)> addProject <title> <date> <teamIC> <tasks>
                                <tasks>: <task1>,<task2>,<task3>...

        addTeam         Creates a new team
                        (Admin)> addTeam <teamname> <member1>,<member2>,<member3>...

        addTask         Adds a new task to the project selected
                        (Admin)> addTask <taskname> <date> <desc>

        changeName      Changes the name of the project or team selected
                        (Admin)> changeName <newname>

        changeDue       Changes the project completion date for the selected project
                        (Admin)> changeDue <newdate>

                        Date format: YYYY/MM/DD

        setDue          Set the due date for a task
                        (Admin)> setDue <taskname> <date>

                        Date format: YYYY/MM/DD

        assign          Assigns the selected project to a team
                        (Admin)> assign <teamname>

        remove          Removes the selected project or team
                        (Admin)> remove

        removeTask      Removes a task from the selected project
                        (Admin)> removeTask <taskname>

        removeMember    Removes a member from the selected team
                        (Admin)> removeMember <name> <position>
 
        editDesc        Edit the description of a task
                        (Admin)> editDesc <taskname> <newdesc>

        changePos       Changes the position of a member
                        (Admin)> changePos <name> <position> <newpos>
        """
        return mainMessage



class regular(interface):
    '''
    This class deals with the user interface for regular users, restricting access to methods
    '''
    def __init__(self):
        super().__init__()


    def taskUndone(self, taskname) -> None:
        '''
        Mark a task as not done
        If selected object is not a (project), raise exceptions.WrongSelection

        :param taskname:    Name of the task to uncheck
        :type taskname:     (str)

        :retur:             None
        '''
        if self.getType() == 'p':
            if not taskname:
                self.__active.uncheckTask(taskname)
        
        else:
            print(exceptions.WrongSelection())


    ##Help message
    def getHelp(self) -> str:
        '''
        Returns the help message for regular users

        :return:    (str)
        '''
        mainMessage = mainMessage = """
        WorkFlow terminal
        The command line app that helps streamline your workflow
        
        Commands:
        help        Returns this message when executed

        commit      Saves changes made to the files

        exit        Exits the program without saving changes

        login       Login to your admin account for privileges

        select      Select a project or team to view or modify
                    > select <"project"/"team"> <project title/team name>

        view        View the details of the selected project or team

        viewAll     View all projects or teams, if a team is selected, details of all the teams will be shown, if a project is selected, details of all the projects will be shown

        status      Show project status

        title       Returns the project title

        name        Returns the team name

        members     Shows the details of all members in the selected team

        done        Marks a task as done
                    > done <taskname>

        undone      Marks a task as not done
                    > undone <taskname>
        """
        return mainMessage



class terminalWork():
    '''
    This class handles the running of the program and is the first thing the user will interact with
    '''
    def __init__(self) -> None:

        self.__reg = regular()
        self.__admin = admin()

        self.__commands = ['login', 'commit', 'view', 'viewAll',
        'status', 'title', 'name', 'members', 'done', 'undone', 'admin']

        self.__adCommands = ['addTask','addMember', 'changeName', 'changeDue',
        'assign', 'remove', 'setDue', 'removeTask', 'editDesc','removeMember',
        'changePos']


    def _adminRun(self) -> None:
        '''
        Access admin only commands
        Input formats for the various commands can be found in the help message
        '''
        prompt = "(Admin)> "

        command = str(input(prompt))
        while command != 'exit':
            if command == 'help':
                print(self.__admin.getHelp())
            

            elif command.startswith('addProject'):
                spaces = command.split(' ')
                params = [None, None, None, None]
                for i in range(1, len(spaces)):
                    params[i -1] = spaces[i]

                tasks = spaces[-1].split(',')
                params[3] = tasks


                self.__admin.addProject(params[0], params[1], params[2], params[3])


            elif command.startswith('addTeam'):
                spaces = command.split(' ')
                if len(spaces) < 3:
                    teamname = str(input("Team name: "))
                    members = str(input("Members (split with commas, <member1>,member2>...):\n"))
                    members = members.split(',')

                else:
                    teamname = spaces[1]
                    members = spaces[2].split(',')

                print(teamname, members)
                self.__admin.addTeam(teamname, members)


            elif command in self.__adCommands:
                if not self.__admin._getActive():
                    print("Nothing has been selected")

                elif command.startswith('assign'):
                    if self.__admin.getType() != 't':
                        print('Teams have no method "assign"')

                    else:
                        space = command.find(' ')
                        if space == -1:
                            teamname = None
                        
                        else:
                            teamname = command[space + 1:]

                        self.__admin.assignProject(teamname)

                elif command.startswith('changeName'):
                    space = command.find(' ')
                    if space == -1:
                        newname = None
                    
                    else:
                        newname = command[space + 1:]

                    if self.__admin.getType() == 'p':
                        self.__admin.changeProName(newname)

                    else:
                        self.__admin.changeTeamName(newname)

                elif command.startswith('removeMember'):
                    spaces = command.split(' ')
                    if len(spaces) != 3:
                        name = str(input("Name: "))
                        position = str(input("position: "))

                    else:
                        name = spaces[1]
                        position = spaces[2]

                    self.__admin.removeMember(name, position)

                elif command.startswith('changeDue'):
                    if self.__admin.getType() == 't':
                        print(exceptions.MethodMadness())

                    else:
                        spaces = command.split(' ')
                        try:
                            newdate = spaces[1]

                        except:
                            newdate = str(input("Due date (YYYY/MM/DD): "))

                        self.__admin.changeProDue(newdate)

                elif command.startswith('addTask'):
                    spaces = command.split(' ')
                    params = [None, None , None]
                    for i in range(1, len(spaces)):
                        params[i -1] = spaces[i]

                    if params[0] == None:
                        params[0] = str(input("Task name: "))

                    if params[1] == None:
                        params[1] = str(input("Due date: "))
                    
                    self.__admin.addTask(self.__admin.getTitle(), params[0], params[1], params[2])

                elif command.startswith('addMember'):

                    spaces = command.split(' ')
                    if len(spaces) != 3:
                        name = str(input("Name: "))
                        position = str(input("Position: "))

                    else:
                        name = spaces[1]
                        position = spaces[2]

                    self.__admin.addMember(name, position)

                elif command.startswith('setDue'):
                    spaces = command.split(' ')
                    if len(spaces) != 3:
                        taskname = str(input("Task name: "))
                        date = str(input("Due date (YYYY/MM/DD): "))

                    else:
                        taskname = spaces[1]
                        date = spaces[2]
                    
                    self.__admin.setTaskDue(taskname, date)

                elif command.startswith('editDesc'):
                    count = command.count(' ')
                    if count < 2:
                        taskname = str(input("Task name: "))
                        newdesc = str(input("New description: "))

                    else:
                        space1 = command.find(' ')
                        space2 = command[space1 + 1:].find(' ')
                        taskname = command[space1 + 1: space2]
                        newdesc = command[space2 + 1:]
                    
                    self.__admin.editDesc(taskname, newdesc)

                elif command.startswith('changePos'):
                    spaces = command.split(' ')
                    if len(spaces) != 4:
                        name = str(input("Name: "))
                        position = str(input("Current position: "))
                        newpos = str(input("New position: "))

                    else:
                        name = spaces[1]
                        position = spaces[2]
                        newpos = spaces[3]

                    self.__admin.changePos(name, position, newpos)

                elif command.startswith('removeTask'):
                    spaces = command.split(' ')
                    if len(spaces) != 2:
                        taskname = str(input("Task to be removed: "))

                    else:
                        taskname = space[1]
                    self.__admin.removeTask(taskname)

                elif command == 'remove':
                    if self.__admin.getType() == 'p':
                        self.__admin.removeProject()

                    elif self.__admin.getType() == 't':
                        self.__admin.removeTeam()

                    else:
                        raise exceptions.InvalidType


            elif command[:6] == 'select':
                try:
                    space = command[7:].index(' ')
                    name = command[space:]

                except:
                    space = name = None
                
                datatype = command[7: space]
                self.__admin.selection(datatype, name)
                if self.__admin.getType() == 'p':
                    title = self.__admin.getTitle()
                    name = ''

                else:
                    name = self.__admin.getName()
                    title = ''

                prompt = f'(Admin)> {name}{title}'

            
            elif command == 'addAdmin':
                self.__admin.addAdmin()


            elif command in self.__commands:
                if not self.__reg._getActive():
                    print("Nothing has been selected")

                elif command == 'members':
                    self.__reg.viewMembers()

                elif command == 'viewAll':
                    self.__reg.viewAll()

                elif command == 'view':
                    self.__reg.view()

                elif command == 'status':
                    self.__reg.projectStatus()

                elif command == 'title':
                    if self.__reg.getType() == 'p':
                        title = self.__reg.getTitle()
                        print(f"Title of selected project: {title}")
                    
                    else:
                        print(exceptions.MethodMadness())

                elif command == 'name':
                    if self.__reg.getType() == 't':
                        name = self.__reg.getName()
                        print(f"Name of selected team: {name}")

                    else:
                        print(exceptions.MethodMadness())

                elif command.startswith('done'):
                    spaces = command.split(' ')
                    if len(spaces) != 2:
                        taskname = str(input("Task name: "))

                    else:
                        taskname = spaces[1]

                    self.__reg.taskDone(taskname)

                elif command.startswith('undone'):
                    spaces = command.split(' ')
                    if len(spaces) != 2:
                        taskname = str(input("Task name: "))

                    else:
                        taskname = spaces[1]

                    self.__reg.taskUndone(taskname)

                elif command == 'commit':
                    self.__reg.commit()


            elif command == 'logout':
                option = str(input("Would you like to commit your changes first? (Y/N)\n"))
                if option == 'Y' or option == 'y':
                    self.__admin.commit()

                else:
                    pass

                self.run()


            else:
                print(f"{command} is invalid, type 'help' to get a list of valid commands")


            command = str(input(prompt))


    def run(self):
        print("="*10, "WorkFlow", "="*10)
        prompt = "> "
        command = str(input(prompt))
        while command != 'exit':
            if command == 'help':
                print(self.__reg.getHelp())


            elif command.startswith('select'):
                try:
                    space = command[7:].index(' ')
                    name = command[space:]

                except:
                    space = name = None
                
                datatype = command[7: space]
                self.__reg.selection(datatype, name)
                if self.__reg.getType() == 'p':
                    title = self.__reg.getTitle()
                    name = ''

                else:
                    name = self.__reg.getName()
                    title = ''

                prompt = f"> {name}{title}"


            elif command == 'login' or command == 'admin':
                if self.__admin.validate():
                    self._adminRun()
                    break

                else:
                    print("Invalid username or password")


            elif command in self.__commands:
                if not self.__reg._getActive():
                    print("Nothing has been selected")

                elif command == 'members':
                    self.__reg.viewMembers()

                elif command == 'viewAll':
                    self.__reg.viewAll()

                elif command == 'view':
                    self.__reg.view()

                elif command == 'status':
                    self.__reg.projectStatus()

                elif command == 'title':
                    if self.__reg.getType() == 'p':
                        title = self.__reg.getTitle()
                        print(f"Title of selected project: {title}")
                    
                    else:
                        print(exceptions.MethodMadness())

                elif command == 'name':
                    if self.__reg.getType() == 't':
                        name = self.__reg.getName()
                        print(f"Name of selected team: {name}")

                    else:
                        print(exceptions.MethodMadness())

                elif command.startswith('done'):
                    spaces = command.split(' ')
                    if len(spaces) != 2:
                        taskname = str(input("Task name: "))

                    else:
                        taskname = spaces[1]

                    self.__reg.taskDone(taskname)

                elif command.startswith('undone'):
                    spaces = command.split(' ')
                    if len(spaces) != 2:
                        taskname = str(input("Task name: "))

                    else:
                        taskname = spaces[1]

                    self.__reg.taskUndone(taskname)

                elif command == 'commit':
                    self.__reg.commit()


            else:
                print(f"{command} is an invalid command, type 'help' to get a list of commands")


            command = str(input(prompt))






##Testing
app = terminalWork()
if __name__ == '__main__':
    app.run()
