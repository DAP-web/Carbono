from core.pyba_logic import PybaLogic

class UserLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def insertUser(self, username, email, password, salt):
        database = self.databaseObj
        user = {
            "username":username,
            "useremail":email,
            "password":password,
            "salt":salt
        }
        sql = (
            f"""
                INSERT INTO `sakila`.`user` (`user_name`, `user_email`, `password`, `salt`)
                VALUES
                ('{user["username"]}', '{user["useremail"]}', '{user["password"]}', '{user["salt"]}');
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def getUserByUsername(self, username):
        database = self.databaseObj
        sql = f"SELECT user_name, password, salt FROM sakila.user WHERE user_name = '{username}';"
        result = database.executeQuery(sql)
        if len(result) > 0:
            return result[0]
        else:
            return []