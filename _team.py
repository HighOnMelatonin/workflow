##Classes for a team object

import _project
import exceptions

class member:
    def __init__(self, name = str(), position = str(), tasks = list()):
        self.__name = name
        self.__position = position
        self.__tasks = tasks


    def getName(self):
        return self.__name
    
    def setName(self, name):
        self.__name = name


    def getPosition(self):
        return self.__position

    def setPostion(self, position):
        self.__position = position

    
    def addTask(self, title, date, desc):
        task = _project.task(title, date, desc)
        self.__tasks.append(task)

    def removeTask(self, title):
        for i in range(len(self.__tasks)):
            if self.__tasks[i].gettitle() == title:
                self.__tasks.pop(i)

        




class team:
    def __str__(self):
        return str((self.__size, self.__members, self.__projects, self.__teamname))

    def __init__(self):
        '''
        self.__size stores the size of the team
        self.__members stores a list of all member objects in the team
        self.__projects stores a list of the titles of the projects the team is in charge of
        self.__teamname stores the name of the team
        '''
        self.__size = int()
        self.__members = list()
        self.__projects = list()
        self.__teamname = str()
    

    def getSize(self) -> int:
        return self.__size


    def getMembers(self) -> list:
        '''
        Returns a list of all member objects

        :return:    List(member)
        '''
        return self.__members

    def addMember(self, name, position) -> None:
        newmember = member(name, position)
        self.__members.append(newmember)
        self.__size += 1

    def removeMember(self, name, position) -> None:
        '''
        Removes member, raises exceptions.Ghost if member cannot be found, no return value
        
        :param name:    Name of the member to be removed
        :type name:     (str)

        :param postion: Position of the member, in case there's another member with the same name
        :type position: (str)
        '''
        for i in range(self.__size):
            if self.__members[i].getName() == name and self.__members[i].getPosition() == position:
                self.__members.pop(i)
                return

        raise exceptions.Ghost
    
    def changePos(self, name, position, newpos) -> None:
        for i in range(len(self.__members)):
            if self.__members[i].getName() == name and self.__members[i].getPosition() == position:
                self.__members[i].setpos(newpos)
                return

        raise exceptions.Ghost

    def getMember(self, name, position):
        '''
        Returns the member object of the member with the specified name and position
        Raises exceptions.Ghost if member cannot be found

        :param name:        Name of member
        :type name:         (str)

        :param position:    Member's position
        :type position:     (str)
        '''
        for i in range(len(self.__members)):
            if self.__members[i].getName() == name and self.__members[i].getPosition() == position:
                return self.__members[i]

        raise exceptions.Ghost


    def getProjects(self) -> list:
        '''
        Returns a list of projects

        :return:    List(project)
        '''
        return self.__projects

    def addProject(self, title) -> None:
        self.__projects.append(title)

    def removeProject(self, title) -> None:
        self.projects.remove(title)


    def getName(self) -> str:
        '''
        Returns the team name

        :return:    (str)
        '''
        return self.__teamname

    def setName(self, teamname) -> None:
        '''
        Changes the team name

        :param teamname:    The new name
        :type teamname:     (str)
        '''
        self.__teamname = teamname


    def display(self) -> None:
        '''
        Prints the details of the team

        :return: None
        '''
        print(f"""{self.getName()}:

        Projects:
        {self.__projects}
        {'='*82}
        Members:
        """)
        for member in self.__members:
            print(f"{member.getName():<30}{member.getPosition():>20}")

