from core.pyba_logic import PybaLogic


class UserLogic(PybaLogic):
    def __init__(self):
        super().__init__()

    def insertUser(self, username, email, password, salt, admin):
        database = self.databaseObj
        user = {
            "username": username,
            "useremail": email,
            "password": password,
            "salt": salt,
            "admin": admin
        }
        sql = (
            f"""
            INSERT INTO `user` (`username`, `email`, `password`,`salt`, `admin`, `creation`) 
            VALUES ('{user["username"]}', '{user["useremail"]}', '{user["password"]}', '{user["salt"]}',
            '{user["admin"]}', current_date());
            """
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def getUserByEmail(self, email):
        database = self.databaseObj
        sql = (f"""
            SELECT userid, username, email, password, salt, admin 
            FROM user where `email` like '{email}';
            """)
        result = database.executeQuery(sql)
        if len(result) > 0:
            return result[0]
        else:
            return []

    def getUsersClients(self):
        database = self.databaseObj
        sql = (f"SELECT * FROM user where admin = 0;")
        result = database.executeQuery(sql)
        if len(result) > 0:
            return result
        else:
            return []

    def deleteUserClient(self, id):
        database = self.databaseObj
        sql = (f"DELETE FROM `user` WHERE userid={id};")
        rows = database.executeNonQueryRows(sql)
        return rows
