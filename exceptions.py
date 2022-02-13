##Exceptions for workflow

class InvalidProjectName(Exception):
    def __str__(self):
        message = "Project does not exist"
        return message


class GhostTeam(Exception):
    def __str__(self):
        message = "Team does not exist"
        return message


class Ghost(Exception):
    def __str__(self):
        message = "The person with the specified position or name does not exist"
        return message


class NoSuchTask(Exception):
    def __str__(self):
        message = "There is no such task in the project"
        return message


class InvalidDate(Exception):
    def __str__(self):
        '''
        If the date input is in the wrong format (YYYY/MM/DD)
        DOES NOT CHECK IF THE DATE IS A VALID DATE, that is for datetime to do
        '''
        message = "Date entered is invalid"
        return message


class MethodMadness(Exception):
    def __str__(self):
        message = "No such methods exist"
        return message


class InvalidType(Exception):
    def __str__(self):
        message = "You have requested for something that doesn't exist in our system right now"
        return message




