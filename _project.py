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

    def getstatus(self):
        return self.__done

    
    def settitle(self, title):
        self.__title = title

    def gettitle(self):
        return self.__title


    def getdescription(self):
        return self.__description

    def setdescription(self, desc):
        self.__description = desc


    def setdue(self, date):
        ##parameter date should be a tuple or a list of length 3 of integers in format (YYYY,MM,DD)
        self.__due = datetime.date(date[0], date[1], date[2])

    def getdue(self):
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
    def _gettask(self, taskname):
        for i in range(len(self.__tasks)):
            if self.__tasks[i] == taskname:
                return i

        raise exceptions.NoSuchTask


    ##Modify the project
    def gettitle(self):
        return self.__title

    def settitle(self, title):
        self.__title = title


    def getteam(self):
        return self.__teamic

    def setteam(self, teamname):
        self.__teamic = teamname

    
    def getdue(self):
        return (self.__due.year, self.__due.month, self.__due.day)

    def setdue(self, date):
        ##parameter date should be a tuple or a list of length 3 of integers in format (YYYY,MM,DD)
        self.__due = datetime.date(date[0], date[1], date[2])


    def getStatus(self):
        done = 0
        total = 0
        for task in self.__tasks:
            total += 1

            if task.getstatus():
                done += 1

        return (done/total)
    

    def display(self):
        print(f"""{self.gettitle()}:

Team in charge: {self.getteam()}
Due date: {self.getdue()}

{'Project status':<50}|{self.getstatus()*100:>20.2f}% complete""")

        print(f"{'Task':<50}|{'Completed':>30}")
        print('='*82)

        for task in self.__tasks:
            print(f"{task.gettitle():<50}|{str(task.getstatus()):>30}")
    

    ##Modify tasks
    def addtask(self, taskname, date, desc):
        self.__tasks.append(task(taskname, date, desc))

    def gettasks(self):
        return self.__tasks

    def removetask(self, taskname):
        i = self._gettask(taskname)
        self.__tasks.pop(i)
        return

    def checktask(self, taskname):
        i = self._gettask(taskname)
        status = self.__tasks[i].getstatus()
        title = self.__tasks[i].gettitle()
        due = self.__tasks[i].getdue()
        desc = self.__tasks[i].getdescription()

        return (status, title, due, desc)

    def taskDone(self, taskname):
        i = self._gettask(taskname)
        self.__tasks[i].check()

        print(f"{self.__tasks[i].gettitle()} is done")

    def taskUndone(self, taskname):
        i = self._gettask(taskname)
        self.__tasks[i].uncheck()

        print(f"{self.__tasks[i].gettitle()} is not done")

    def setdesc(self, taskname, newdesc):
        i = self._gettask(taskname)
        self.__tasks[i].setdescription(newdesc)

    def settaskdue(self, taskname, date):
        i = self._gettask(taskname)
        self.__tasks[i].setdue(date)

