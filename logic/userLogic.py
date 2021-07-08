from core.pyba_logic import PybaLogic

class UserLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def insertUser(self, username, email, password, salt, admin):
        database = self.databaseObj
        user = {
            "username":username,
            "useremail":email,
            "password":password,
            "salt":salt,
            "admin": admin
        }
        sql = (
            f"""
            INSERT INTO `carbonodb`.`user` (`username`, `email`, `password`,`salt`, `admin`) 
            VALUES ('{user["username"]}', '{user["useremail"]}', '{user["password"]}', '{user["salt"]}',
            '{user["admin"]}');
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def getUserByEmail(self, email):
        database = self.databaseObj()
        sql = (
            "SELECT email, password, salt "
            + f"FROM carbonodb where email like '{email}';"
        )
        result = database.executeQuery(sql)
        if len(result) > 0:
            return result[0]
        else:
            return []

    