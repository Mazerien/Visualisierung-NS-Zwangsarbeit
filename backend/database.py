"""
Control for the MySQL server listening in TCP/3306.
Credentials in dotenv.
"""

import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from datetime import date


class MySQL:
    """
    Handles all connections with the MySQL database.
    """
    pool: MySQLConnectionPool = None
    tables: list[str] = ["Person", "Company",
                         "Employment", "Housing", "Tenancy", "Imprisonment"]

    def __init__(self, user: str, password: str, host: str, db: str):
        """
        Starts a connection pool within the MySQL database. Allows for faster read/write.
        """
        try:
            self.pool = MySQLConnectionPool(
                pool_name="pool",
                pool_size=3,
                user=user,
                password=password,
                host=host,
                database=db,
            )

        except mysql.connector.errors.DatabaseError as e:
            print(e)
            print(f"Can't connect to MySQL. Continuing without database.")

    def query_exec(self, query: str, values=None, is_read_only: bool = False):
        """
        Executes a given query query; immediately commits to DB.
        query: Query string
        values: Value strings if given.
        is_read_only: Commits a change only if one is given; defaults to false.
        """
        if self.pool is None:
            print(f"No DB connection. Query '{query}' not executed.")
            return

        cnx: PooledMySQLConnection = self.pool.get_connection()
        cur = cnx.cursor()
        cur.execute(query, values)
        match is_read_only:
            case True:
                cur = cur.fetchall()
                cnx.close()
                return cur
            case False:
                cnx.commit()
                cnx.close()

    def check_tables(self):
        """
        Checks if all tables exist. Creates them if they don't.
        """
        try:
            for table in self.tables:
                self.query_exec(f"SELECT * FROM {table}", is_read_only=True)
        except mysql.connector.errors.ProgrammingError:
            print("No tables exist in this DB. Creating them now.")
            self.create_tables()

    def create_tables(self):
        """
        Creates the tables as specified by the DB schema in the README.
        """
        cnx = self.pool.get_connection()
        cur = cnx.cursor()

        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS `Person` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,

    `LastName` varchar(255) NOT NULL,
    `FirstName` varchar(255) NOT NULL,
    `MaidenName` varchar(255),
    `Gender` enum('M', 'F', 'X') NOT NULL,

    `PlaceOfBirth` varchar(255),
    `DateOfBirth` date,
    `PlaceOfDeath` varchar(255),
    `DateOfDeath` date,
    `Nationality` varchar(255),
    `LastPlaceOfResidence` varchar(255),

    `Marriage` varchar(255),
    `Father` varchar(255),
    `Mother` varchar(255),
    `Religion` varchar(255),
    `Profession` varchar(255),

    PRIMARY KEY (`ID`)
    ) ENGINE=InnoDB
            """,

            """
            CREATE TABLE IF NOT EXISTS `Company` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `Name` varchar(255) NOT NULL,

    PRIMARY KEY (`ID`)
    ) Engine=InnoDB
            """,

            """
            CREATE TABLE IF NOT EXISTS `Employment` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `Name` varchar(255),
    `Company` int(11) NOT NULL,
    `Person` int(11) NOT NULL,

    PRIMARY KEY (`ID`),
    FOREIGN KEY (`Person`) REFERENCES `Person`(`ID`),
    FOREIGN KEY (`Company`) REFERENCES `Company`(`ID`)
    ) Engine=InnoDB
            """,

            """
            CREATE TABLE IF NOT EXISTS `Housing` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `Adress` varchar(255) NOT NULL,
    `Type` enum('Schwenningen', 'Imprisonment', 'Living') NOT NULL,

    PRIMARY KEY (`ID`)
    ) Engine=InnoDB
            """,

            """
            CREATE TABLE IF NOT EXISTS `Tenancy` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `Housing` int(11) NOT NULL,
    `Person` int(11) NOT NULL,
    `StartDate` date,
    `EndDate` date,

    PRIMARY KEY (`ID`),
    FOREIGN KEY (`Housing`) REFERENCES `Housing`(`ID`),
    FOREIGN KEY (`Person`) REFERENCES `Person`(`ID`)
    ) Engine=InnoDB   
            """,

            """
            CREATE TABLE IF NOT EXISTS `Imprisonment` (
    `ID` int(11) NOT NULL AUTO_INCREMENT,
    `Person` int(11) NOT NULL,
    `PrisonerID` int(11),
    `StartDate` date,
    `EndDate` date,
    `AgeAtImprisonment` int(11),
    `PrisonerOfWar` bool,
    `CourtOfLaw` varchar(255),

    PRIMARY KEY (`ID`),
    FOREIGN KEY (`Person`) REFERENCES `Person`(`ID`)
    ) Engine=InnoDB
            """
        ]
        for table in table_queries:
            self.query_exec(table)

    def insert_person(self, last_name: str, name: str, maiden_name: str, gender: chr, place_of_birth: str,
                      date_of_birth: date, place_of_death: str, date_of_death: date, nationality: str,
                      last_place_of_residence: str, marriage: str, father: str, mother: str, religion: str,
                      profession: str):
        """
        Inserts a single Person with their respective data.
        Refer to the MySQL schema for more information.
        """
        query = """INSERT INTO Person (LastName, FirstName, MaidenName, Gender, PlaceOfBirth, DateOfBirth, 
        PlaceOfDeath, DateOfDeath, Nationality, LastPlaceOfResidence, Marriage, Father, Mother, Religion, Profession
        ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
        values = (last_name, name, maiden_name, gender, place_of_birth, date_of_birth, place_of_death, date_of_death,
                  nationality, last_place_of_residence, marriage, father, mother, religion, profession)
        self.query_exec(query, values)

    def insert_company(self, name: str):
        """
        Inserts into the Company table.
        """
        query = "INSERT INTO Company (Name) VALUES (%s)"
        values = (name,)
        self.query_exec(query, values)

    def insert_employment(self, name: str, company_id: int, person_id: int):
        """
        Inserts into the Employment table. An Employment has a Person, a Company, and optionally, a job title.
        """
        query = "INSERT INTO Employment (Name, Company, Person) VALUES (%s, %s, %s)"
        values = (name, company_id, person_id)
        self.query_exec(query, values)

    def insert_housing(self, adress: str, housing_type: str):
        """
        Inserts a house with its respective housing type.
        """
        query: str = "INSERT INTO Housing (Adress, Type) VALUES (%s, %s)"
        values = (adress, housing_type)
        self.query_exec(query, values)

    def insert_tenancy(self, housing_id: int, person_id: int, start_date: date, end_date: date):
        """
        Inserts a tenancy record with housing, person, start date, and end date.
        """
        query: str = "INSERT INTO Tenancy (Housing, Person, StartDate, EndDate) VALUES (%s, %s, %s, %s)"
        values = (housing_id, person_id, start_date, end_date)
        self.query_exec(query, values)

    def insert_imprisonment(self, person_id: int, prisoner_id: int, start_date: date, end_date: date,
                            age_at_imprisonment: int, prisoner_of_war: bool, court_of_law: str):
        """
        Inserts an imprisonment record with person, prisoner ID, start date, end date, age at imprisonment,
        whether the person was a prisoner of war, and the court of law.
        """
        query: str = """
        INSERT INTO Imprisonment (Person, PrisonerID, StartDate, EndDate, AgeAtImprisonment, PrisonerOfWar, CourtOfLaw)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (person_id, prisoner_id, start_date, end_date,
                  age_at_imprisonment, prisoner_of_war, court_of_law)
        self.query_exec(query, values)

    def select_columns_in_table(self, table_name: str):
        """
        Gets the columns information of a specified table.
        """
        query: str = (
            f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';"
        )
        return self.query_exec(query, is_read_only=True)

    def select_rows_in_table(self, table_name: str):
        """
        Gets all rows from a specified table.
        """
        query: str = f"SELECT * FROM {table_name};"
        return self.query_exec(query, is_read_only=True)

    def drop_tables(self, reset_db: bool = True):
        """
        Deletes all tables and associated data.
        Also re-creates tables if reset_db.
        """
        # List reversed because later tables are dependent on former ones
        for table in reversed(self.tables):
            self.query_exec(f"DROP TABLE IF EXISTS {table}")
        if reset_db:
            self.create_tables()

    def get_person_by_name(self, first_name: str, maiden_name: str, last_name: str):
        """
        Checks if a person by that exact name exists in the DB.
        """
        if maiden_name:
            query: str = "SELECT * FROM Person WHERE FirstName = %s AND MaidenName = %s AND LastName = %s"
            values: tuple[str, str, str] = (first_name, maiden_name, last_name)
        else:
            query: str = "SELECT * FROM Person WHERE FirstName = %s AND LastName = %s"
            values: tuple[str, str] = (first_name, last_name)
        return self.query_exec(query, values, is_read_only=True)

    def get_company_by_name(self, name: str):
        """
        Checks if a company by that exact name exists in the DB.
        """
        query: str = "SELECT * FROM Company WHERE Name = %s"
        values: tuple[str] = (name,)
        return self.query_exec(query, values, is_read_only=True)

    def get_employment_by_id(self, company_id: int, person_id: int):
        """
        Gets an Employment with a given Company and Person key pair.
        """
        query: str = "SELECT * FROM Employment WHERE Company = %s AND Person = %s"
        values: tuple[int, int] = (company_id, person_id)
        return self.query_exec(query, values, is_read_only=True)

    def get_housing_by_adress(self, adress: str):
        """
        Retrieve a housing record by its address.
        """
        query: str = "SELECT * FROM Housing WHERE Adress = %s"
        values = (adress,)
        return self.query_exec(query, values, is_read_only=True)

    def get_tenancy_by_id(self, housing_id: int, person_id: int):
        """
        Retrieve a tenancy record by housing and person identifiers.
        """
        query: str = "SELECT * FROM Tenancy WHERE Housing = %s AND Person = %s"
        values = (housing_id, person_id)
        return self.query_exec(query, values, is_read_only=True)
