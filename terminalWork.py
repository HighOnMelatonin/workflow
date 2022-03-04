'''
the command line interface version



Workflow is a command line app that helps to streamline concurrent projects and task to various teams in an organisation
Should have an interface for admins and one for regular team members so that members from a different team cannot set a task as done for a project that wasn't assigned to them

'''

import exceptions
import sqlite3
import _team
import _project
from getpass import getpass
import handler


class interface:
    '''
    This class deals with the user interface

    Methods allowed in this class:
    1. Viewing projects and tasks
    2. Marking tasks as done
    3. Checking project status

    self.__active is the project or teamname that is currently being modified
    self.__background is everthing else, all the other projects and teams

    separating self.__active from self.__background so that the user can modify the same project or team without having to repeatedly input the team/project name
    '''
    def __init__(self):
        self.__background = handler.handler()
        self.__active = None


    ##Active
    def _changeActive(self, new, datatype):
        '''
        Changes the value of self.__active to the object selected

        :param new:         The title of the project or team name
        :type new:          (str)

        :param datatype:    Determines whether its a project or team
        :type datatype:     (str)

        :return:            None
        '''
        if datatype == 'p' or datatype == 'project':
            self.__active = self.__background.getProject(new)

        elif datatype == 't' or datatype == 'team':
            self.__active = self.__background.getTeam(new)

        else:
            raise exceptions.InvalidType

    def _getActive(self):
        return self.__active


    ##Get input
    def _getDate(self) -> tuple:
        date = str(input("Date (YYYY/MM/DD): "))

        date = date.split('/')

        for i in range(len(date)):
            date[i] = int(date[i])

        return date

    def _getTask(self):
        '''
        Shows a list of all the tasks and returns user's choice
        '''
        tasks = self.__background.allTasks()
        print(tasks)
        taskname = str(input("Task name: "))
        return taskname


    ##Selection
    def selection(self, datatype = None, name = None) -> None:
        '''
        Change the active object being modified

        :param datatype:    Selection of a project or a team
        :type datatype:     (str)

        :param name:        Project title or team name
        :type name:         (str)

        :return:            None
        '''
        if not datatype:
            datatype = str(input("Do you want to modify a project or a team?\n"))

        if datatype == 'project' and not name:
            projects = self.__background.allProjects()
            print("List of projects: ")
            for project in projects:
                print(project.getTitle())

            name = str(input("Selection: "))

        elif datatype == 'team' and not name:
            teams = self.__background.allTeams()
            print("List of teams: ")
            for team in teams:
                print(team.getName())

        else:
            raise exceptions.InvalidType

        #interface._changeActive already catches invalid names
        self._changeActive(name, datatype)


    ##View
    def view(self):
        '''
        Displays details of a project or a team, depending on what has been selected
        '''
        if type(self.__active) == _project.project:
            project = self.__background.getProject(self.__active.getTitle())
            project.display()

        elif type(self.__active) == _team.team:
            team = self.__background.getTeam(self.__active.getName())
            

        else:
            raise exceptions.MethodMadness(exceptions.WrongSelection)


    def viewAll(self):
        '''
        View all projects or teams
        '''
        if type(self.__active) == _team.team:
            teams = self.__background.allTeams()
            for team in teams:
                team.display()

        elif type(self.__active) == _project.project:
            projects = self.__background.allProjects()
            for project in projects:
                project.display()

        else:
            raise exceptions.InvalidType


    ##Project
    def projectStatus(self):
        status = self.__active.getStatus()
        print(f"{self.__active.getTitle()} is {status*100:.2f}% complete")

    def getTitle(self):
        '''
        Return project title for the selected project
        '''
        return self.__active.getTitle()


    ##Team
    def getName(self):
        '''
        Return team name for the selected team
        '''
        return self.__active.getName()


    ##Member
    def viewMembers(self) -> None:
        '''
        View all members (without team names)
        '''
        if type(self.__active) == _project.project:
            raise exceptions.InvalidType

        else:
            members = self.__background.allMembers()
            print(f"{'Name':<30}{'Position':>20}")
            for member in members:
                print(f"{member.getName():<30}{member.getPosition():>20}")


    ##Editing
    #Tasks
    def taskDone(self, taskname):
        self.__active.checkTask(taskname)


    ##Commit
    def commit(self):
        self.__background.commit()


class admin(interface):
    '''
    This class deals with the user interface for admins, making more methods available
    
    Methods allowed in this class (on top of interface):
    1. Adding new tasks and projects
    2. Editing teams
    3. Assigning teams to projects
    4. Adding new admins
    5. Making new teams
    '''
    def __init__(self):
        super().__init__()


    ##Private methods
    def _checkAdmin(self, name, password):
        db = sqlite3.connect('misc/data/admins.db')
        cursor = db.execute("SELECT * FROM ACCOUNTS")
        allAdmin = cursor.fetchall()
        if (name, password) in allAdmin:
            return True

        else:
            return False

    def _addAdmin(self, name, password):
        db = sqlite3.connect('misc/data/admins.db')
        cursor = db.execute('SELECT * FROM ACCOUNTS')
        for account in cursor:
            if account[0] == name:
                if self._checkAdmin(name, password):
                    print("Admin account with the same name exists, attempting to sign you in...")
                    return self._checkAdmin(name, password)

                else:
                    raise exceptions.Clone

        else:
            db.execute(f"""INSERT INTO ACCOUNTS
            VALUES({name}, {password})""")
            db.commit()
            print("New account added")


    def _encode(self, password):
        encoded = ''
        for char in password:
            newchar = str(ord(char))
            encoded += newchar.ljust(3, '0')

        return encoded

    def _decode(self, encoded):
        password = ''
        for i in range(len(encoded), step = 3):
            char = chr(int(encoded[i: i + 3]))
            password += char

        return password


    ##Validate admin
    def validate(self):
        '''
        Checks if the user is an admin
        '''
        name = str(input("Name: "))
        password = getpass('Password (hidden): ')

        return self._checkAdmin(name, self._encode(password))


    ##Add new
    ##Project
    def addProject(self, title = None, date = None, teamic = None, tasks = []):
        '''
        Creates a new project, param title must be filled

        :param title:   Project title
        :type title:    (str)

        :param date:    Date of completion
        :type date:     Tuple(int, int, int)

        :param teamic:  Team in charge of the project
        :type teamic:   (str)

        :param tasks:   Subtasks to be completed for the project
        :type tasks:    list(task)
        '''
        if not title:
            title = str(input("Project title: "))
        
        self.__background.addProject(title, date, teamic, tasks)


    ##Admin
    def addAdmin(self):
        '''
        Only an admin can add a new admin
        '''
        name = str(input("Name (for logging in): "))
        pass1 = getpass('Password (hidden): ')
        pass2 = getpass('Re-enter password (hidden): ')

        if pass1 != pass2:
            self.addAdmin()

        else:
            self._addAdmin(name, pass1)

    
    ##Team
    def addTeam(self, teamname = None, members = []):
        '''
        Make a new team


        '''
        if not teamname:
            teamname = str(input("Team name: "))

        self.__background.addTeam(teamname)

        for member in members:
            self.__background.addMember(teamname, member[0], member[1])


    ##Task
    def addTask(self, title = None, taskname = None, date = None, desc = None):
        '''
        Add a new task to the project

        :param title:      Title of the project
        :type title:        (str)

        :param taskname:    Name of the task to be added
        :type taskname:     (str)

        :param date:        Due date for the task in YYYY/MM/DD format
        :type date:         tuple(int, int, int)

        :param desc:        Description of the task
        :type desc:         (str)
        '''
        if not title:
            title = str(input("Project title: "))

        if not taskname:
            taskname = str(input("Task name: "))

        if not date:
            date = str(input("Date (YYYY/MM/DD): "))

            date = date.split('/')

            for i in range(len(date)):
                date[i] = int(date[i])

        self.__background.addTask(self.__active.getTitle(), taskname, tuple(date), desc)


    ##Member
    def addMember(self, name = None, position = None) -> None:
        '''
        :param name:        Name of the new member
        :type name:         (str)

        :param position:    New member's position
        :type position:     (str)
        '''
        if not name:
            name = str(input("Name: "))

        if not position:
            position = str((input("Position: ")))
        
        self.__background.addMember(self.__active.getName(), name, position)


    ##Modifications
    ##Project
    def changeProName(self, newtitle = None) -> None:
        '''
        :param newtitle:    New project title
        :type newtitle:     (str)
        '''
        if not newtitle:
            newtitle = str(input("New title: "))

        self.__background.changeProName(self.__active.getTitle(), newtitle)

    def changeProDue(self, date = None) -> None:
        '''
        :param date:    Project completion date, in YYYY/MM/DD/ format
        :type date:     Tuple(int, int, int)
        '''
        if not date:
            date = self._getDate()

        self.__background.setProdue(self.__active.getTitle(), tuple(date))

    def assignProject(self, teamic = None) -> None:
        '''
        Assigns the project to a team

        :param teamic:  The name of the team in charge
        :type teamic:   (str)
        '''
        if not teamic:
            teams = self.__background.allTeams()
            print(teams)
            teamic = str(input("Team in-charge: "))

        self.__background.assignProject(teamic, self.__active.getTitle())

    def removeProject(self):
        '''
        Removes the current project
        '''
        self.__background.removeProject(self.__active.getTitle())


    ##Tasks
    def setTaskDue(self, taskname = None, date = None) -> None:
        if not taskname:
            taskname = self._getTask()

        if not date:
            date = self._getDate()
        
        self.__background.setTaskDue(self.__active.getTitle(), taskname, date)
    
    def removeTask(self, taskname):
        if not taskname:
            taskname = self._getTask()

        self.__background.removeTask(self.__active.getTitle(), taskname)

    def editDesc(self, taskname = None, newdesc = None):
        if not taskname:
            taskname = self._getTask()

        if not newdesc:
            newdesc = str(input("New description: "))

        self.__background.editDesc(self.__active.getTitle(), taskname, newdesc)


    ##Teams
    def removeTeam(self):
        '''
        Removes the selected team
        '''
        self.__background.removeTeam(self.__active.getName())

    def changeTeamName(self, newname = None):
        '''
        :param newname: The new team name
        :type newname:  (str)
        '''
        if not newname:
            newname = str(input("New team name: "))

        self.__background.changeTeamName(self.__active.getName(), newname)


    ##Member
    def removeMember(self, membername, position):
        '''
        Removes a member from the team

        :param membername:  Name of the member to be removed
        :type membername:   (str)

        :param position:    Member's position, in case there are members in the team with the same name
        :type position:     (str)
        '''
        if not membername:
            membername = str(input("Member name: "))

        if not position:
            position = str(input("Member's position: "))

        self.__background.removeMember(self.__active.getName(), membername, position)

    def changePos(self, membername, position, newpos):
        '''
        :param membername:  Name of the member
        :type membername:   (str)

        :param position:    Member's position
        :type position:     (str)

        :param newpos:      New position
        :type newpos:       (str)
        '''
        if not membername:
            membername = str(input("Member name: "))

        if not position:
            position = str(input("Member's position: "))

        if not newpos:
            newpos = str(input("Member's new position: "))

        self.__background.changePos(self.__active.getName, membername, position, newpos)


    ##Help message
    def getHelp(self):
        mainMessage = """
        WorkFlow terminal
        The command line app that helps streamline your workflow
        
        Commands:
        help        Returns this message when executed

        commit      Saves changes made to the files

        exit        Exits the program without saving changes

        login       Login to your admin account for privileges

        start       Starts the program as a regular user with no privileges

        select      Select a project or team to view or modify
                    > select <project/team> <project title/team name>


        Admin commands:
        addAdmin    Adds a new admin to the database, only existing admins can add new admins

        addMember   Adds a new member to the team selected
        """
        return mainMessage

        



class regular(interface):
    '''
    This class deals with the user interface for regular users, restricting access to methods
    
    
    '''
    def __init__(self):
        super().__init__()


    def taskUndone(self, taskname):
        '''
        Mark a task as not done

        :param taskname:    Name of the task to uncheck
        :type taskname:     (str)
        '''
        if not taskname:
            self.__active.uncheckTask(taskname)


    ##Help message
    def getHelp(self):
        mainMessage = """
        WorkFlow terminal
        The command line app that helps streamline your workflow
        
        Commands:
        help        Returns this message when executed

        commit      Saves changes made to the files

        exit        Exits the program without saving changes

        login       Login to your admin account for privileges

        start       Starts the program as a regular user with no privileges

        select      Select a project or team to view or modify
                    > select <project/team> <project title/team name>
        """
        return mainMessage



class terminalWork():
    '''
    This class handles the running of the program and is the first thing the user will interact with
    '''
    def __init__(self):
        self.__reg = regular()
        self.__admin = admin()
        self.__commands = ['help', 'login', 'start', 'select', 'list', 'commit']
        self.__adCommands = ['addMember', 'addAdmin']


    def _adminRun(self):
        '''
        Access admin only commands
        '''
        prompt = "(Admin)> "
        command = str(input(prompt))
        while command != 'exit':
            if command == 'help':
                print(self.__admin.getHelp())
                command = str(input(prompt))
                continue
            
            if command in self.__adCommands:
                print("You're in admin commands")

            elif command[:6] == 'select':
                try:
                    space = command[7:].index(' ')
                    name = command[space:]

                except:
                    space = name = None
                
                datatype = command[7: space]
                self.__admin.selection(datatype, name)

            elif command in self.__commands:
                print("That's a regular command")

            else:
                print(f"{command} is invalid, type 'help' to get a list of valid commands")

            command = str(input(prompt))


    def run(self):
        print("="*10, "WorkFlow", "="*10)
        prompt = "> "
        command = str(input(prompt))
        while command != 'exit':
            if command in self.__commands:
                if command == 'help':
                    print(self.__reg.getHelp())

                elif command == 'start':
                    continue

                elif command == 'login':
                    self.__admin.validate()
                    self._adminRun()
                    break

                elif command[:6] == 'select':
                    try:
                        space = command[7:].index(' ')
                        name = command[space:]

                    except:
                        space = name = None
                    
                    datatype = command[7: space]
                    self.__reg.selection(datatype, name)

                else:
                    print("Hello")

            else:
                print(f"{command} is an invalid command, type 'help' to get a list of commands")

            command = str(input(prompt))




##Testing
app = terminalWork()
if __name__ == '__main__':
    app.run()
