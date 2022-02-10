##Classes for a team object

import _project
import exceptions

class member:
    def __str__(self):
        return str((self.__name, self.__position, self.__tasks))

    def __init__(self, name = str(), position = str(), tasks = list()):
        self.__name = name
        self.__position = position
        self.__tasks = tasks


    def getname(self):
        return self.__name
    
    def setname(self, name):
        self.__name = name


    def getposition(self):
        return self.__position

    def setposition(self, position):
        self.__position = position

    
    def addtask(self, title, date, desc):
        task = _project.task(title, date, desc)
        self.__tasks.append(task)

    def removetask(self, title):
        for i in range(len(self.__tasks)):
            if self.__tasks[i].gettitle() == title:
                self.__tasks.pop(i)

        




class team:
    def __str__(self):
        return str((self.__size, self.__members, self.__projects, self.__teamname))

    def __init__(self):
        self.__size = int()
        self.__members = list()
        self.__projects = list()
        self.__teamname = str()
    

    def getsize(self):
        return self.__size


    def getmembers(self):
        return self.__members

    def addmember(self, name, position):
        newmember = member(name, position)
        self.__members.append(newmember)
        self.__size += 1

    def removemember(self, name, position):

        for i in range(self.__size):
            if self.__members[i].getname() == name and self.__members[i].getposition() == position:
                self.__members.pop(i)
                return

        raise exceptions.Ghost
    


    def addproject(self, title):
        self.__projects.append(title)

    def removeproject(self, title):
        self.projects.remove(title)


    def getname(self):
        return self.__teamname

    def setname(self, teamname):
        self.__teamname = teamname


