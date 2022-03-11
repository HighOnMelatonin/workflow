##Classes for projects

import datetime
import exceptions

class task:
    def __str__(self) -> str:
        return (self.__title, self.__description, self.__done, self.__due)

    def __init__(self, title = str(), date = tuple(), desc = str()) -> None:
        '''
        :param title:   Name of the task
        :type title:    (str)

        :param date:    Due date for the task
        :type date:     Tuple(int, int, int)

        :param desc:    Description of the task
        :type desc:     (str)

        :return:        None
        '''
        self.__title = title
        self.__description = desc
        self.__done = False
        self.__due = datetime.date(date[0], date[1], date[2])


    def check(self) -> None:
        '''
        Mark task as done

        :return:    None
        '''
        self.__done = True

    def uncheck(self) -> None:
        '''
        Mark task as not done

        :return:    None
        '''
        self.__done = False

    def getStatus(self) -> bool:
        '''
        Return the status of task (done or not done)

        :return:    (Bool)
        '''
        return self.__done

    
    def setTitle(self, title) -> None:
        '''
        Change the name of the task

        :param title:   New title for the task
        :type title:    (str)

        :return:        None
        '''
        self.__title = title

    def getTitle(self) -> str:
        '''
        Return the task name

        :return:    (str)
        '''
        return self.__title


    def getDescription(self) -> str:
        '''
        Return the description of the task

        :return:    (str)
        '''
        return self.__description

    def setDescription(self, desc) -> None:
        '''
        Set the description of the task

        :param desc:    New description for the task
        :type desc:     (str)

        :return:        None
        '''
        self.__description = desc


    def setDue(self, date) -> None:
        '''
        Set the due date for the task, in the format (YYYY,MM,DD)
        Converts the tuple into a datetime.date object to be stored

        :param date:    The due date for the task
        :type date:     Tuple(int, int, int)

        :return:        None
        '''
        self.__due = datetime.date(date[0], date[1], date[2])

    def getDue(self) -> tuple:
        '''
        Return the due date of the task

        :return:    Tuple
        '''
        return (self.__due.year, self.__due.month, self.__due.day)



class project:
    def __str__(self):
        return str((self.__title, self.__due, self.__teamic, self.__tasks))
    
    def __init__(self, title, date, teamic, tasks) -> None:
        ##Maybe add an option for user-defined attributes
        '''
        :param title:   Title of the project
        :type title:    (str)

        :param date:    Project completion date
        :type date:     Tuple(int, int, int)

        :param teamic:  Team in charge of the proejct
        :type teamic:   (str)

        :param tasks:   Tasks for the project
        :type tasks:    List(task)
        '''
        self.__title = title
        self.__due = datetime.date(date[0], date[1], date[2])
        self.__teamic = teamic
        self.__tasks = tasks
    

    ##Private methods
    def _getTask(self, taskname) -> int:
        '''
        Return the index of the task in the project, given the task name
        If task cannot be found, raise exceptions.NoSuchTask

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            (int)
        '''
        for i in range(len(self.__tasks)):
            if self.__tasks[i] == taskname:
                return i

        raise exceptions.NoSuchTask


    ##Modify the project
    def getTitle(self) -> str:
        '''
        Return the project title

        :return:    (str)
        '''
        return self.__title

    def setTitle(self, title) -> None:
        '''
        Set the project title

        :param title:   New title for the project
        :type title:    (str)

        :return:        None
        '''
        self.__title = title


    def getTeam(self) -> str:
        '''
        Return the name of the team in charge

        :return:    (str)
        '''
        return self.__teamic

    def setTeam(self, teamname) -> None:
        '''
        Change the team in charge

        :param teamname:    Name of the team
        :type teamname:     (str)

        :return:            None
        '''
        self.__teamic = teamname

    
    def getDue(self) -> tuple:
        '''
        Return the completion date for the project

        :return:    Tuple
        '''
        return (self.__due.year, self.__due.month, self.__due.day)

    def setDue(self, date) -> None:
        '''
        Set the completion date for the project, in (YYYY,MM,DD) format

        :param date:    The completion date for the project
        :type date:     Tuple(int, int, int)

        :return:        None
        '''
        self.__due = datetime.date(date[0], date[1], date[2])


    def getStatus(self) -> float:
        '''
        Return the project status, the percentage of tasks done
        If the project has no tasks, raise exceptions.EmptyProject

        :return:    (float)
        '''
        done = 0
        total = 0
        for task in self.__tasks:
            total += 1

            if task.getStatus():
                done += 1
        
        if total == 0:
            raise exceptions.EmptyProject
        
        return (done/total)
    

    def display(self) -> None:
        '''
        Print the details of the task

        :return:    None
        '''
        print(f"""{self.getTitle()}:

Team in charge: {self.getTeam()}
Due date: {self.getDue()}

{'Project status':<50}|{self.getStatus()*100:>20.2f}% complete""")

        print(f"{'Task':<50}|{'Completed':>30}")
        print('='*82)

        for task in self.__tasks:
            print(f"{task.getTitle():<50}|{str(task.getStatus()):>30}")
    

    ##Modify tasks
    def addTask(self, taskname, date, desc) -> None:
        '''
        Add a task to the project

        :param taskname:    Name of the task
        :type taskname:     (str)

        :param date:        Due date for the task
        :type date:         Tuple(int, int, int)

        :param desc:        Task description
        :type desc:         (str)

        :return:            None
        '''
        self.__tasks.append(task(taskname, date, desc))

    def getTasks(self) -> list:
        '''
        Return the list of tasks

        :return:    List(task)
        '''
        return self.__tasks

    def removeTask(self, taskname) -> None:
        '''
        Removes a task from the project

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            None
        '''
        i = self._getTask(taskname)
        self.__tasks.pop(i)
        return

    def checkTask(self, taskname):
        '''
        Get the details of a task

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            (task)
        '''
        i = self._getTask(taskname)
        status = self.__tasks[i].getStatus()
        title = self.__tasks[i].getTitle()
        due = self.__tasks[i].getDue()
        desc = self.__tasks[i].getDescription()

        return (status, title, due, desc)

    def taskDone(self, taskname) -> None:
        '''
        Mark a task as done

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            None
        '''
        i = self._getTask(taskname)
        self.__tasks[i].check()

        print(f"{self.__tasks[i].getTitle()} is done")

    def taskUndone(self, taskname) -> None:
        '''
        Mark a task as not done

        :param taskname:    Name of the task
        :type taskname:     (str)

        :return:            None
        '''
        i = self._getTask(taskname)
        self.__tasks[i].uncheck()

        print(f"{self.__tasks[i].getTitle()} is not done")

    def setDesc(self, taskname, newdesc) -> None:
        '''
        Set the description for a task

        :param taskname:    Name of the task
        :type taskname:     (str)

        :param newdesc:     The new task description
        :type newdesc:      (str)

        :return:            None
        '''
        i = self._getTask(taskname)
        self.__tasks[i].setDescription(newdesc)

    def setTaskDue(self, taskname, date) -> None:
        '''
        Set the due date for a task

        :param taskname:    Name of the task
        :type taskname:     (str)

        :param date:        The new due date for the task
        :type date:         Tuple(int, int, int)

        :return:            None
        '''
        i = self._getTask(taskname)
        self.__tasks[i].setDue(date)

