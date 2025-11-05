""" 
Control for the MySQL server listening in TCP/3306.
Credentials in dotenv.
"""
import mysql.connector

class MySQL:
    """
    Handles all connections with the MySQL database.
    """
    user: str = ""
    password: str = ""
    host: str = ""
    db: str = ""

    def __init__(self, user: str, password: str, host: str, db: str):
        self.user = user
        self.password = password
        self.host = host
        self. db = db

    def connect(self):
        """
        TODO: Docstring
        """
        try:
            cnx = mysql.connector.connect(
                user=self.user, password=self.password, host=self.host, database=self.db)
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
