""" 
Control for the PostgreSQL server listening in TCP/5432.
Credentials in dotenv.
"""
import psycopg

class PSQL:
    """
    Handles all connections with the PostgreSQL database.
    """
    user: str = ""
    password: str = ""
    db: str = ""

    def __init__(self, user: str=None, password: str=None, db: str=None):
        """
        Credentials in dotenv; check README for instructions.
        """
        if user is None or password is None or db is None:
            raise FileNotFoundError("Can't find .env data. Does it exist?")
        self.user = user
        self.password = password
        self.db = db


    def create_table(self):
        """
        TODO: Docstring
        """
        with psycopg.connect(
            user=self.user,
            password=self.password,
            port=5432,
            dbname=self.db,
            host="db"
            ) as conn:
            pass
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS test (
                        id serial PRIMARY KEY,
                        num integer,
                        data text
                    )"""
                )
                cur.execute(
                    """
                    INSERT INTO test (num, data) VALUES (%s, %s)
                    """, (100, "abc'def"))
                cur.execute("SELECT * FROM test")
                print(cur.fetchone()
                )