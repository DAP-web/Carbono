from core.pyba_logic import PybaLogic

class TaskLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def getAllTasksByUser(self, userid):
        database = self.createDatabaseObj()
<<<<<<< HEAD
        sql = f"select * from carbonodb.tasks where userid=1 order by priority asc;"
=======
        sql = f"select * from carbonodb.tasks where userid={userid};"
>>>>>>> de23fb684a2a94c6876eb4a08552cfdb300253af
        result = database.executeQuery(sql)
        return result

    def getTaskById(self, taskid):
        database = self.createDatabaseObj()
        sql = f"select * from tasks where taskid={taskid};"
        result = database.executeQuery(sql)
        return result

    def insertTask(self, userid, date, task, priority, estado):
        database = self.databaseObj
        tasks = {
            "userid": userid,
            "date": date,
            "task": task,
            "priority": priority,
            "estado": estado
        }
        sql = (
            f"""
                INSERT INTO `carbonodb`.`tasks` (`userid`, `date`, `task`, `priority`, `estado`)
                VALUES
                ('{tasks["userid"]}', 
                '{tasks["date"]}', 
                '{tasks["task"]}', 
                '{tasks["priority"]}', 
                '{tasks["estado"]}');
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateTask(self, taskid, nuevoEstado):
        database = self.createDatabaseObj()
        sql = (
            f"""
            UPDATE `carbonodb`.`tasks` SET `estado` = '{nuevoEstado}' WHERE `taskid` = '{taskid}';
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    # def deleteTask(self, taskid):
    #     database = self.createDatabaseObj()
    #     sql = f"delete from tasks where taskid={taskid};"
    #     rows = database.executeNonQueryRows(sql)
    #     return rows