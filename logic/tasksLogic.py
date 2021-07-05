from core.pyba_logic import PybaLogic

class TaskLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def getTaskById(self, taskid):
        database = self.createDatabaseObj()
        sql = f"select * from tasks where taskid={taskid};"
        result = database.executeQuery(sql)
        return result

    def insertTask(self, userid, date, task, priority):
        database = self.databaseObj
        user = {
            "userid":userid,
            "date":date,
            "task":task,
            "priority":priority
        }
        sql = (
            f"""
                INSERT INTO `carbonodb`.`tasks` (`userid`, `date`, `task`, `priority`)
                VALUES
                ('{tasks["userid"]}', '{tasks["date"]}', '{tasks["task"]}', '{tasks["priority"]}');
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    
    def updateTask(self, taskid, tasks):
        database = self.createDatabaseObj()
        sql = (
            f"UPDATE `carbonodb`.`tasks` "
            + f"SET `userid` = '{tasks['userid']}', `date` = '{tasks['date']}', "
            + f"`task` = {tasks['task']}, `priority` = {tasks['priority']} "
            + f"WHERE `taskid` = {taskid};"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def deleteTask(self, taskid):
        database = self.createDatabaseObj()
        sql = f"delete from tasks where taskid={taskid};"
        rows = database.executeNonQueryRows(sql)
        return rows