import mysql.connector
from mysql.connector import Error


class Database:
    HOST = "sql.freedb.tech"
    USER = "freedb_kareemelnaghy"
    PASSWORD = "MGGsm25HZZZW&x4"
    DATABASE = "freedb_oscars"

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.HOST,
            user=self.USER,
            password=self.PASSWORD,
            database=self.DATABASE
        )
        if self.connection.is_connected():
            self.cursor = self.connection.cursor(dictionary=True)
            print("DB Connected")
            return True
        else:
            print("Failed to connect")
            return False

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("DB connection closed")

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return True

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def add_user(self, email, username, birthDate, gender, country): # query to add a user
        query = """INSERT INTO user (email, username, birthDate, gender, country) 
                   VALUES (%s, %s, %s, %s, %s)"""
        return self.execute_query(query, (email, username, birthDate, gender, country))

    def get_user(self, username): # query to fetch a user
        query = "SELECT * FROM user WHERE username = %s"
        return self.fetch_one(query, (username,))

    def add_nomination(self, movieTitle, releaseYear, firstName, lastName, email, categoryName, iteration):
        query = """INSERT INTO user_nomination 
                   (movieTitle, releaseYear, firstName, lastName, email, categoryName, iteration) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        return self.execute_query(query, (movieTitle, releaseYear, firstName, lastName, email, categoryName, iteration))

    def get_user_nominations(self, email):
        query = """SELECT movieTitle, releaseYear, firstName, lastName, 
                          categoryName, iteration 
                   FROM user_nomination
                   WHERE email = %s"""
        return self.fetch_all(query, (email,))

    def get_top_nominated_movies(self):
        query = """SELECT movieTitle, releaseYear, COUNT(*) as nomination_count 
                   FROM user_nomination
                   GROUP BY movieTitle, releaseYear 
                   ORDER BY nomination_count DESC 
                   LIMIT 10
                   """
        return self.fetch_all(query)

    def get_staff_member_stats(self, firstName, lastName):
        query = """SELECT 
                       COUNT(DISTINCT n.movieTitle, n.releaseYear, n.categoryName) as total_nominations,
                       SUM(CASE WHEN n.isWinner = 'yes' THEN 1 ELSE 0 END) as total_oscars
                   FROM nomination n
                   WHERE n.firstName = %s AND n.lastName = %s"""
        return self.fetch_one(query, (firstName, lastName))

    def get_top_birth_countries(self):
        query = """SELECT p.birthCountry, COUNT(*) as winner_count
                   FROM person p
                   INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
                   WHERE n.categoryName = 'Best Actor in a Leading Role' AND n.isWinner = 'yes'
                   GROUP BY p.birthCountry
                   ORDER BY winner_count DESC
                   LIMIT 5"""
        return self.fetch_all(query)

    def get_nominated_staff_by_country(self, country):
        query = """SELECT p.firstName, p.lastName, 
                          GROUP_CONCAT(DISTINCT n.categoryName) as categories,
                          COUNT(DISTINCT n.movieTitle, n.releaseYear, n.categoryName) as nomination_count,
                          SUM(CASE WHEN n.isWinner = 'yes' THEN 1 ELSE 0 END) as oscar_count
                   FROM person p
                   INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
                   WHERE p.birthCountry = %s
                   GROUP BY p.firstName, p.lastName
                   ORDER BY oscar_count DESC, nomination_count DESC"""
        return self.fetch_all(query, (country,))

    def get_dream_team(self):
        # use several query to retrieve best staff members in each category (living)
        dream_team = {}
        # Best Director
        director_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        WHERE n.categoryName = 'Best Directing' 
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        director = self.fetch_one(director_query)
        if director:
            dream_team['Director'] = {
                'firstName': director['firstName'],
                'lastName': director['lastName'],
                'oscar_count': director['oscar_count']
            }

        # Best Actor and Actress
        actor_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        INNER JOIN person_role pr ON p.firstName = pr.firstName AND p.lastName = pr.lastName
        WHERE pr.roleType = 'Actor' 
        AND n.categoryName = 'Best Actor in a Leading Role'
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        actor = self.fetch_one(actor_query)
        if actor:
            dream_team['Leading Actor'] = {
                'firstName': actor['firstName'],
                'lastName': actor['lastName'],
                'oscar_count': actor['oscar_count']
            }

        actress_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        INNER JOIN person_role pr ON p.firstName = pr.firstName AND p.lastName = pr.lastName
        WHERE pr.roleType = 'Actress' 
        AND n.categoryName = 'Best Actress in a Leading Role'
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        actress = self.fetch_one(actress_query)
        if actress:
            dream_team['Leading Actress'] = {
                'firstName': actress['firstName'],
                'lastName': actress['lastName'],
                'oscar_count': actress['oscar_count']
            }

        # Best Supporting Actor and Actress
        supp_actor_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        WHERE n.categoryName = 'Best Actor in a Supporting Role'
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        supp_actor = self.fetch_one(supp_actor_query)
        if supp_actor:
            dream_team['Supporting Actor'] = {
                'firstName': supp_actor['firstName'],
                'lastName': supp_actor['lastName'],
                'oscar_count': supp_actor['oscar_count']
            }

        supp_actress_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        WHERE n.categoryName = 'Best Actress in a Supporting Role'
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        supp_actress = self.fetch_one(supp_actress_query)
        if supp_actress:
            dream_team['Supporting Actress'] = {
                'firstName': supp_actress['firstName'],
                'lastName': supp_actress['lastName'],
                'oscar_count': supp_actress['oscar_count']
            }

        # Best Picture Producer
        producer_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        INNER JOIN person_role pr ON p.firstName = pr.firstName AND p.lastName = pr.lastName
        WHERE pr.roleType = 'Producer' 
        AND n.categoryName = 'Best Picture'
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        producer = self.fetch_one(producer_query)
        if producer:
            dream_team['Producer'] = {
                'firstName': producer['firstName'],
                'lastName': producer['lastName'],
                'oscar_count': producer['oscar_count']
            }

        # Best Original Score Composer
        composer_query = """
        SELECT p.firstName, p.lastName, COUNT(*) as oscar_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        INNER JOIN person_role pr ON p.firstName = pr.firstName AND p.lastName = pr.lastName
        WHERE pr.roleType = 'Composer' 
        AND (n.categoryName LIKE '%Score%' OR n.categoryName LIKE '%Music%')
        AND n.isWinner = 'yes'
        AND p.deathDate IS NULL
        GROUP BY p.firstName, p.lastName
        ORDER BY oscar_count DESC
        LIMIT 1
        """
        composer = self.fetch_one(composer_query)
        if composer:
            dream_team['Composer'] = {
                'firstName': composer['firstName'],
                'lastName': composer['lastName'],
                'oscar_count': composer['oscar_count']
            }
            # return dream team list
        return dream_team

    def check_movie_exists(self, movie_title, release_year): # helper function that executes a query to validate existence of a movie
        query = "SELECT 1 FROM movie WHERE movieTitle = %s AND releaseYear = %s"
        result = self.fetch_one(query, (movie_title, release_year))
        return result is not None

    def check_person_exists(self, first_name, last_name): # helper function that executes a query to validate existence of a person
        query = "SELECT 1 FROM person WHERE firstName = %s AND lastName = %s"
        result = self.fetch_one(query, (first_name, last_name))
        return result is not None

    def get_top_nominated_movies_by_category_iteration(self):
        query = """
        SELECT movieTitle, releaseYear, categoryName, iteration, COUNT(*) as nomination_count
        FROM user_nomination
        GROUP BY movieTitle, releaseYear, categoryName, iteration
        ORDER BY categoryName, iteration, nomination_count DESC
        """
        return self.fetch_all(query)

    def get_staff_member_stats(self, first_name, last_name):
        query = """
        SELECT 
            pr.roleType,
            COUNT(DISTINCT n.movieTitle, n.releaseYear, n.categoryName) as total_nominations,
            SUM(CASE WHEN n.isWinner = 'yes' THEN 1 ELSE 0 END) as total_oscars
        FROM person p
        INNER JOIN person_role pr ON p.firstName = pr.firstName AND p.lastName = pr.lastName
        LEFT JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        WHERE p.firstName = %s AND p.lastName = %s
        AND pr.roleType IN ('Singer', 'Composer', 'Director', 'Actor', 'Actress')
        GROUP BY pr.roleType
        """
        return self.fetch_all(query, (first_name, last_name))

    def get_top_birth_countries_for_best_actor(self):
        query = """
        SELECT 
            p.birthCountry, 
            COUNT(*) as winner_count
        FROM person p
        INNER JOIN nomination n ON p.firstName = n.firstName AND p.lastName = n.lastName
        WHERE n.categoryName = 'Best Actor in a Leading Role' AND n.isWinner = 'yes'
        GROUP BY p.birthCountry
        ORDER BY winner_count DESC
        LIMIT 5
        """
        return self.fetch_all(query)

    def get_top_production_companies(self):
        query = """
        SELECT 
            pc.companyName, 
            COUNT(*) as oscar_count
        FROM production_company pc
        INNER JOIN nomination n ON pc.movieTitle = n.movieTitle AND pc.releaseYear = n.releaseYear
        WHERE n.isWinner = 'yes'
        GROUP BY pc.companyName
        ORDER BY oscar_count DESC
        LIMIT 5
        """
        return self.fetch_all(query)

    def get_non_english_oscar_winners(self):
        query = """
        SELECT DISTINCT 
            m.movieTitle, 
            m.releaseYear, 
            m.language
        FROM movie m
        INNER JOIN nomination n ON m.movieTitle = n.movieTitle AND m.releaseYear = n.releaseYear
        WHERE m.language != 'English' AND n.isWinner = 'yes'
        ORDER BY m.releaseYear DESC, m.movieTitle
        """
        return self.fetch_all(query)