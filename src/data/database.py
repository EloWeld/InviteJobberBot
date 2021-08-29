import sqlite3

from aiogram import types


class Database():
    def __init__(self, path_to_db="Data.db"):
        super(Database, self).__init__()
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())


# ==================== POOL DATABASE ==================== #
class UsersDatabase(Database):
    def __init__(self):
        super().__init__()
        pass

    def add_user(self, user: types.User):
        sql = 'INSERT INTO users(id, username, fullname, deposit) VALUES(?, ?, ?, ?)'
        params = (user.id, user.username, user.full_name, 0)
        self.execute(sql, parameters=params, commit=True)

    def all_users(self):
        sql = 'SELECT DISTINCT * FROM users'
        db_out = self.execute(sql, fetchall=True)
        result = [{
            'id':        db_r[0],
            'username':  db_r[1],
            'fullname':  db_r[2],
            'polls':     db_r[3],
            'privilege': db_r[4],
            'deposit':   db_r[5]
        } for db_r in db_out]
        return result

    def filter(self, column, value):
        sql = f'SELECT * FROM users WHERE {column} = "{str(value)}"'
        db_out = self.execute(sql, fetchall=True)
        result = [{
            'id':        db_r[0],
            'username':  db_r[1],
            'fullname':  db_r[2],
            'polls':     db_r[3],
            'privilege': db_r[4],
            'deposit':   db_r[5]
        } for db_r in db_out]
        return result

    def get_0user_data(self, value, column, key='id'):
        sql = f'SELECT {column} FROM users WHERE {key} = "{str(value)}"'
        try:
            db_out = self.execute(sql, fetchall=True)[0][0]
        except:
            # Failed
            db_out = None

        return db_out

    def get_user_data(self, value, column, key='id'):
        sql = f'SELECT {column} FROM users WHERE {key} = "{str(value)}"'
        try:
            db_out = [x[0] for x in self.execute(sql, fetchall=True)]
        except:
            # Failed
            db_out = None

        return db_out


    def filter_remove(self, column, value):
        sql = f'DELETE FROM users WHERE {column} = "{str(value)}"'
        self.execute(sql, commit=True)

    def update_field(self, user_id, field, new_value):
        sql = f'UPDATE users SET {field} = "{str(new_value)}" WHERE id = "{str(user_id)}"'
        self.execute(sql, commit=True)


# ==================== CHECK DATABASE ==================== #
class CheckDatabase(Database):
    def __init__(self):
        super().__init__()
        pass

    def add_check(self, poll_id, owner_id, check, price):
        sql = 'INSERT INTO btc_checks(poll_id, owner_id, check, price) VALUES(?, ?, ?, ?)'
        params = (poll_id, owner_id, check, price)
        self.execute(sql, parameters=params, commit=True)

    def get_check(self, select_colmun, key, value):
        sql = f'SELECT {select_colmun} FROM btc_checks WHERE {key} = "{str(value)}"'
        try:
            db_out = self.execute(sql, fetchall=True)[0][0]
        except:
            # Failed
            db_out = None

        return db_out

    def all_checks(self):
        sql = f'SELECT * FROM btc_checks'
        try:
            db_out = []
            for entity in self.execute(sql, fetchall=True):
                db_out.append({'id': entity[0],
                               'poll_id': entity[1],
                               'owner_id': entity[2],
                               'check': entity[3],
                               'price': entity[4]})

        except:
            # Failed
            db_out = None

        return db_out

    def remove_check(self, key, value):
        sql = f'DELETE FROM btc_checks WHERE {key} = "{str(value)}"'
        self.execute(sql, commit=True)


# ==================== POOL DATABASE ==================== #
class PoolDatabase(Database):
    def __init__(self):
        super().__init__()
        pass

    def save_poll(self, dt : dict):
        sql = 'INSERT INTO polls(' \
              'owner_id, color, diffic, wages, time, desc, contact, ' \
              'vacancy, price, sub_type, sub_len, posting_time, status) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        params = (dt["owner_id"],
                  dt["color"],
                  dt["difficulty"],
                  dt["wages"],
                  dt["time"],
                  dt["desc"],
                  dt["contact"],
                  dt["vacancy"],
                  dt["price"],
                  dt["sub_type"],
                  dt["sub_len"],
                  dt["posting_time"],
                  dt["status"])
        self.execute(sql, parameters=params, commit=True)

    def update_status(self, id: int, status):
        sql = f'UPDATE polls SET status = "{str(status)}" WHERE id = "{str(id)}"'
        self.execute(sql, commit=True)

    def update_poll_field(self, poll_id, field, new_value):
        sql = f'UPDATE polls SET {field} = "{str(new_value)}" WHERE id = "{str(poll_id)}"'
        self.execute(sql, commit=True)

    def update_poll_field2(self, owner_id, field, new_value):
        sql = f'UPDATE polls SET {field} = "{str(new_value)}" WHERE owner_id = "{str(owner_id)}"'
        self.execute(sql, commit=True)

    def polls_filter(self, column, value):
        sql = f'SELECT * FROM polls WHERE {column} = "{str(value)}"'
        db_out = self.execute(sql, fetchall=True)
        result = [{
            'id':           db_r[0],
            'owner_id':     db_r[1],
            'color':        db_r[2],
            'difficulty':   db_r[3],
            'wages':        db_r[4],
            'time':         db_r[5],
            'desc':         db_r[6],
            'contact':      db_r[7],
            'vacancy':      db_r[8],
            'price':        db_r[9],
            'sub_type':     db_r[10],
            'sub_len':      db_r[11],
            'posting_time': db_r[12],
            'status':       db_r[13],
            'pub_time':     db_r[14],
        } for db_r in db_out]
        return result

    def polls_filter_remove(self, key, value):
        sql = f'DELETE FROM polls WHERE {key} = "{str(value)}"'
        self.execute(sql, commit=True)


PollDB = PoolDatabase()
UsersDB = UsersDatabase()
CheckDB = CheckDatabase()