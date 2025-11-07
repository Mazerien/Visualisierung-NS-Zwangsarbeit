""" 
Control for the MySQL server listening in TCP/3306.
Credentials in dotenv.
"""
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool


class MySQL:
    """
    Handles all connections with the MySQL database.
    """
    pool: MySQLConnectionPool = None

    def __init__(self, user: str, password: str, host: str, db: str):
        """
        Starts a connection pool within the MySQL database. Allows for faster read/write.
        """
        self.pool = MySQLConnectionPool(
            pool_name="pool", pool_size=3, user=user, password=password, host=host, database=db)

    def query_exec(self, query: str, is_read_only: bool = False):
        """
        Executes a given query string; immediately commits to DB.
        query: Query string
        is_read_only: Commits a change only if one is given; defaults to false.
        """
        cnx: MySQLConnectionPool.PooledMySQLConnection = self.pool.get_connection()
        cur = cnx.cursor()
        cur.execute(query)
        match is_read_only:
            case True:
                cur = cur.fetchall()
                cnx.close()
                return cur
            case False:
                cnx.commit()
                cnx.close()

    def connect(self):
        """
        TODO: Docstring
        """
        try:
            cnx = self.pool.get_connection()
            print("Connected to MySQL database.")
            cur = cnx.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS `person` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `first_name` varchar(14) NOT NULL,
    `last_name` varchar(14) NOT NULL,
    `date_of_birth` date NOT NULL,
    `gender` enum('M', 'F', 'X'),
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB""")
            cnx.commit()
        except mysql.connector.Error as e:
            print(e)
            print("No MySQL database connection possible. Continuing without database.")

    def create_demo_data(self):
        """
        Demo data for testing.
        """
        self.query_exec("""
    INSERT INTO person (first_name, last_name, date_of_birth, gender) VALUES
    ('Alice', 'Johnson', '1995-04-12', 'F'),
    ('Bob', 'Smith', '1988-11-23', 'M'),
    ('Charlie', 'Brown', '2000-06-05', 'X'),
    ('Diana', 'White', '1992-01-30', 'F'),
    ('Ethan', 'Williams', '1985-09-17', 'M');
    """)

    def get_columns_in_table(self, table_name: str):
        """
        Gets the columns information of a specified table.
        table_name: Name of the table.
        """
        query: str = f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
        return self.query_exec(query, True)

    def get_rows_in_table(self, table_name: str):
        """
        Gets all rows from a specified table.
        """
        query: str = f"SELECT * FROM {table_name};"
        return self.query_exec(query, True)
