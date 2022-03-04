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
    

    def getSize(self):
        return self.__size


    def getMembers(self):
        '''
        Returns a list of all member objects
        '''
        return self.__members

    def addMember(self, name, position):
        newmember = member(name, position)
        self.__members.append(newmember)
        self.__size += 1

    def removeMember(self, name, position):

        for i in range(self.__size):
            if self.__members[i].getName() == name and self.__members[i].getPosition() == position:
                self.__members.pop(i)
                return

        raise exceptions.Ghost
    
    def changePos(self, name, position, newpos):
        for i in range(len(self.__members)):
            if self.__members[i].getName() == name and self.__members[i].getPosition() == position:
                self.__members[i].setpos(newpos)
                return

        raise exceptions.Ghost

    def getMember(self, name, position):
        for i in range(len(self.__members)):
            if self.__members[i].getName() == name and self.__members[i].getPosition() == position:
                return self.__members[i]

        raise exceptions.Ghost


    def getProjects(self):
        return self.__projects

    def addProject(self, title):
        self.__projects.append(title)

    def removeProject(self, title):
        self.projects.remove(title)


    def getName(self):
        return self.__teamname

    def setName(self, teamname):
        self.__teamname = teamname


    def display(self):
        print(f"""{self.getName()}:

        Projects:
        {self.__projects}
        {'='*82}
        Members:
        """)
        for member in self.__members:
            print(f"{member.getName():<30}{member.getPosition():>20}")

t = team()
team.addMember('Hello','Kenobi','general')
team.display()