""" 
Control for the PostgreSQL server listening in TCP/5432.
Credentials in dotenv.
"""
import psycopg

class SQL:
    """
    TODO: Docstring
    """
    user: str = ""
    password: str = ""

    def __init__(self, user: str=None, password: str=None):
        """
        TODO: Docstring
        """
        if user is None or password is None:
            raise("Can't find .env data. Does it exist?")
        self.user = user
        self.password = password


    def create_table(self):
        """
        TODO: Docstring
        """
        with psycopg.connect(host="localhost", port=5432) as conn:
            pass
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE test (
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