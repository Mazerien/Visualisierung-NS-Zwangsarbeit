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
        if not is_read_only:
            cnx.commit()
            return
        return cnx.fetchall()

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

    def create_table():
        """
        TODO: Docstring
        """
        # TODO: Proper DB tables, right now just used for testing
        table: str = """
CREATE TABLE 'person' (
'id' int(11) NOT NULL AUTO_INCREMENT,
'first_name' varchar(14) NOT NULL,
'last_name' varchar(14) NOT NULL,
'date_of_birth' date NOT NULL,
'gender' enum('M', 'F', 'X')
PRIMARY KEY ('id')
) ENGINE=InnoDB"""
        pass

    def create_demo_data(self):
        """
        Demo data for testing.
        """
        pass
        self.query_exec()

    def get_columns_in_table(self):
        """
        TODO: Docstrings"""
        pass
        query: str = "SELECT count(*) FROM person;"
        return self.query_exec(query, True)