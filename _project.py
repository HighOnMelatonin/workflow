##Classes for projects

import datetime
import exceptions

class task:
    def __str__(self):
        return (self.__title, self.__description, self.__done, self.__due)

    def __init__(self, title = str(), date = tuple(), desc = str()):
        self.__title = title
        self.__description = desc
        self.__done = False
        self.__due = datetime.date(date[0], date[1], date[2])


    def check(self):
        self.__done = True

    def uncheck(self):
        self.__done = False

    def getStatus(self):
        return self.__done

    
    def setTitle(self, title):
        self.__title = title

    def getTitle(self):
        return self.__title


    def getDescription(self):
        return self.__description

    def setDescription(self, desc):
        self.__description = desc


    def setDue(self, date):
        ##parameter date should be a tuple or a list of length 3 of integers in format (YYYY,MM,DD)
        self.__due = datetime.date(date[0], date[1], date[2])

    def getDue(self):
        return (self.__due.year, self.__due.month, self.__due.day)



class project:
    def __str__(self):
        return str((self.__title, self.__due, self.__teamic, self.__tasks))
    
    def __init__(self, title, date, teamic, tasks):
        ##Maybe add an option for user-defined attributes
        self.__title = title
        self.__due = datetime.date(date[0], date[1], date[2])
        self.__teamic = teamic
        self.__tasks = tasks
    

    ##Private methods
    def _getTask(self, taskname):
        for i in range(len(self.__tasks)):
            if self.__tasks[i] == taskname:
                return i

        raise exceptions.NoSuchTask


    ##Modify the project
    def getTitle(self):
        return self.__title

    def setTitle(self, title):
        self.__title = title


    def getTeam(self):
        return self.__teamic

    def setTeam(self, teamname):
        self.__teamic = teamname

    
    def getDue(self):
        return (self.__due.year, self.__due.month, self.__due.day)

    def setDue(self, date):
        ##parameter date should be a tuple or a list of length 3 of integers in format (YYYY,MM,DD)
        self.__due = datetime.date(date[0], date[1], date[2])


    def getStatus(self):
        done = 0
        total = 0
        for task in self.__tasks:
            total += 1

            if task.getStatus():
                done += 1
        
        if total == 0:
            raise exceptions.EmptyProject
        
        return (done/total)
    

    def display(self):
        print(f"""{self.getTitle()}:

Team in charge: {self.getTeam()}
Due date: {self.getDue()}

{'Project status':<50}|{self.getStatus()*100:>20.2f}% complete""")

        print(f"{'Task':<50}|{'Completed':>30}")
        print('='*82)

        for task in self.__tasks:
            print(f"{task.getTitle():<50}|{str(task.getStatus()):>30}")
    

    ##Modify tasks
    def addTask(self, taskname, date, desc):
        self.__tasks.append(task(taskname, date, desc))

    def getTasks(self):
        return self.__tasks

    def removeTask(self, taskname):
        i = self._getTask(taskname)
        self.__tasks.pop(i)
        return

    def checkTask(self, taskname):
        i = self._getTask(taskname)
        status = self.__tasks[i].getStatus()
        title = self.__tasks[i].getTitle()
        due = self.__tasks[i].getDue()
        desc = self.__tasks[i].getDescription()

        return (status, title, due, desc)

    def taskDone(self, taskname):
        i = self._getTask(taskname)
        self.__tasks[i].check()

        print(f"{self.__tasks[i].getTitle()} is done")

    def taskUndone(self, taskname):
        i = self._getTask(taskname)
        self.__tasks[i].uncheck()

        print(f"{self.__tasks[i].getTitle()} is not done")

    def setDesc(self, taskname, newdesc):
        i = self._getTask(taskname)
        self.__tasks[i].setDescription(newdesc)

    def setTaskDue(self, taskname, date):
        i = self._getTask(taskname)
        self.__tasks[i].setDue(date)

