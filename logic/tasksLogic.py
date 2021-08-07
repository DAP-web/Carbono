from core.pyba_logic import PybaLogic


class TaskLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def getAllTasksClients(self):
        database = self.createDatabaseObj()
        sql = f"""SELECT tasks.taskid, tasks.userid, user.username, user.admin, tasks.date, tasks.priority, tasks.task, tasks.estado, tasks.categoria
                    FROM tasks inner join user on tasks.userid = user.userid
                    WHERE user.admin <> 1;
                """
        result = database.executeQuery(sql)
        return result

    def getAllTasksByUser(self, userid):
        database = self.createDatabaseObj()
        sql = f"select * from tasks where userid={userid} order by priority asc;"
        result = database.executeQuery(sql)
        return result

    def getTaskById(self, taskid):
        database = self.createDatabaseObj()
        sql = f"select * from tasks where taskid={taskid};"
        result = database.executeQuery(sql)
        return result

    def insertTask(self, userid, date, task, priority, estado, categoria):
        database = self.databaseObj
        tasks = {
            "userid": userid,
            "date": date,
            "task": task,
            "priority": priority,
            "estado": estado,
            "categoria": categoria
        }
        sql = (
            f"""
                INSERT INTO `tasks` (`userid`, `date`, `task`, `priority`, `estado`, `categoria`)
                VALUES
                ('{tasks["userid"]}', 
                '{tasks["date"]}', 
                '{tasks["task"]}', 
                '{tasks["priority"]}', 
                '{tasks["estado"]}',
                '{tasks["categoria"]}');
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateTask(self, taskid):
        database = self.createDatabaseObj()
        sql = (
            f"""
            UPDATE `tasks` SET `estado` = 1 WHERE `taskid` = '{taskid}';
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def traerCategorias(self):
        database = self.createDatabaseObj()
        sql = f"SELECT DISTINCT categoria FROM tasks;"
        result = database.executeQuery(sql)
        return result

    def deleteTask(self, taskid):
        database = self.createDatabaseObj()
        sql = f"DELETE FROM `tasks` WHERE `taskid` = '{taskid}';"
        rows = database.executeNonQueryRows(sql)
        return rows
