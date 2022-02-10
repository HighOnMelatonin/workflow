
class InvalidProjectName(Exception):
    def __str__(self):
        message = "Project does not exist"
        return message


class InvalidTeamName(Exception):
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

