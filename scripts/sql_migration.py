"""Script to migrate data from the .xlsx into MySQL."""
import mysql.connector
import json
from datetime import date


class MySQL:
    """
    Handles all connections with the MySQL database.
    """

    pool = None
    tables: list[str] = ["person", "company",
                         "employment", "housing", "tenancy", "imprisonment"]

    def __init__(self, user: str, password: str, host: str, db: str):
        """
        Starts a connection pool within the MySQL database. Allows for faster read/write.
        """
        try:
            self.pool = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db
            )
            self.check_tables()
        except Exception as e:
            print(e)
            print("Can't connect to MySQL. Continuing without database.")

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

        cnx = self.pool
        cur = cnx.cursor()
        cur.execute(query, values)
        match is_read_only:
            case True:
                cur = cur.fetchall()
                return cur
            case False:
                cnx.commit()

    def check_tables(self):
        """
        Checks if all tables exist. Creates them if they don't.
        """
        try:
            for table in self.tables:
                self.query_exec(f"SELECT * FROM {table}", is_read_only=True)
                print(f"Table {table} found. Continuing.")
        except mysql.connector.errors.ProgrammingError:
            print("No tables exist in this DB. Creating them now.")
            self.create_tables()

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

    def create_tables(self):
        """Goes through every schema and creates a SQL table for them."""
        cur = self.pool.cursor()
        with open("schema.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        for table in self.tables:
            insert_string = " ".join(data[table])
            cur.execute(insert_string)

    def insert_person(self, last_name: str, first_name: str, maiden_name: str, gender: chr,
                      place_birth: str, date_birth: date, place_death: str,
                      nationality: str, last_place_residence: str, marriage: str, father: str,
                      mother: str, religion: str, profession: str):
        """
        Inserts a single Person with their respective data.
        Refer to the MySQL schema for more information.
        """
        query = """INSERT INTO person (
        last_name, first_name, maiden_name, gender, place_birth, date_birth, place_death,
        nationality, last_place_residence, religion, profession
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            last_name, first_name, maiden_name, gender, place_birth, date_birth,
            place_death, nationality, last_place_residence, religion,
            profession
        )
        self.query_exec(query, values)

    def get_person_by_name(self, first_name: str, maiden_name: str, last_name: str):
        if maiden_name:
            query: str = "SELECT * FROM person WHERE first_name = %s AND maiden_name = %s AND last_name = %s"
            values: tuple[str, str, str] = (first_name, maiden_name, last_name)
        else:
            query: str = "SELECT * FROM person WHERE first_name = %s AND last_name = %s"
            values: tuple[str, str] = (first_name, last_name)
        return self.query_exec(query, values, is_read_only=True)

    def get_person_by_id(self, person_id: int):
        query: str = "SELECT * FROM person WHERE id = %s"
        values = (person_id,)
        return self.query_exec(query, values, is_read_only=True)

    def insert_company(self, name: str):
        query = "INSERT INTO company (name_comp_hist) VALUES (%s)"
        values = (name,)
        self.query_exec(query, values)

    def get_company_by_name(self, name: str):
        """Checks if a company by that exact name exists in the DB."""
        query: str = "SELECT * FROM company WHERE name_comp_hist = %s"
        values: tuple[str] = (name,)
        return self.query_exec(query, values, is_read_only=True)

    def insert_housing(self, name_place: str, location: str):
        """Checks if a housing by that exact name exists in the DB."""
        query = "INSERT INTO housing (name_place, location) VALUES (%s, %s)"
        values = (name_place, location)
        self.query_exec(query, values)

    def get_housing_by_adress(self, adress: str):
        """
        Retrieve a housing record by its address.
        """
        query: str = "SELECT * FROM housing WHERE name_place = %s"
        values = (adress,)
        return self.query_exec(query, values, is_read_only=True)

    def insert_employment(self, occupation: str, company_id: int, person_id: int):
        """
        Inserts into the Employment table.
        """
        query: str = """INSERT INTO employment
        (occupation, company_id, person_id) VALUES (%s, %s, %s)
        """
        values = (occupation, company_id, person_id)
        self.query_exec(query, values)

    def get_employment_by_id(self, company_id: int, person_id: int):
        """
        Gets an Employment with a given Company and Person key pair.
        """
        query: str = "SELECT * FROM employment WHERE company_id = %s AND person_id = %s"
        values: tuple[int, int] = (company_id, person_id)
        return self.query_exec(query, values, is_read_only=True)

    def insert_tenancy(self, housing_id: int, person_id: int, start_date: date, end_date: date):
        query: str = "INSERT INTO tenancy (housing_id, person_id, start_date, end_date) VALUES (%s, %s, %s, %s)"
        values = (housing_id, person_id, start_date, end_date)
        self.query_exec(query, values)
    
    def get_tenancy_by_id(self, housing_id: int, person_id: int):
        query: str = "SELECT * FROM tenancy WHERE housing_id = %s AND person_id = %s"
        values = (housing_id, person_id)
        return self.query_exec(query, values, is_read_only=True)
