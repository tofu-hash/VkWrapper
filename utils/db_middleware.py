import sqlite3


def connect(timeout: int = 10) -> tuple:
    db: sqlite3.Connection = sqlite3.connect('database.db', timeout=timeout)
    return db, db.cursor()


def disconnect(db: sqlite3.Connection, cur: sqlite3.Cursor):
    cur.close()
    db.close()


def execute(request: str, fetchone: bool = False, fetchall: bool = False, commit: bool = True):
    db, cur = connect()
    response = cur.execute(request)

    if commit:
        db.commit()

    if fetchone:
        response = cur.fetchone()
    elif fetchall:
        response = cur.fetchall()
    return response


def make_tables_schema(schema_file: str = 'schema.sql'):
    with open(schema_file, 'r') as sqlite_file:
        sql_script = sqlite_file.read()

    db, cur = connect()
    cur.executescript(sql_script)


# if __name__ == '__main__':
make_tables_schema()
