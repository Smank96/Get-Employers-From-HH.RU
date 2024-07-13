import psycopg2
import re
from src.read_config import read_config
from src.utils import validate_salary


class DBManager:
    def __init__(self):
        params = read_config()
        self.dbconnect = psycopg2.connect(**params)
        self.cursor = self.dbconnect.cursor()

    def create_tables(self):
        """Создание таблиц."""
        sql_query = """
            CREATE TABLE IF NOT EXISTS employers
            (
                employer_id serial PRIMARY KEY,
                employer_name varchar,
                employer_url varchar,
                vacancies_url varchar,
                open_vacancies int
            );

            CREATE TABLE IF NOT EXISTS vacancies
            (
                vacancy_id serial PRIMARY KEY,
                vacancy_name varchar,
                city varchar,
                employer_id serial,
                salary int,
                currency varchar,
                publication_date date,
                vacancy_url varchar,
                requirement text,
                responsibility text,
                required_experience varchar,
                CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers(employer_id)
            );"""

        self.cursor.execute(sql_query)
        self.dbconnect.commit()

    def drop_tables(self):
        sql_query = ("""DROP TABLE IF EXISTS employers CASCADE;
        DROP TABLE IF EXISTS vacancies CASCADE;""")

        self.cursor.execute(sql_query)
        self.dbconnect.commit()

    def save_data_to_database(self, employers: list[dict], vacancies: list[dict]):
        """Добавление данных в sql таблицы."""
        employer_index = 0

        for employer in employers:
            # получаем данные из словаря employers.
            employer_name = employer.get('name')
            employer_url = employer.get('alternate_url')
            vacancies_url = employer.get('vacancies_url')
            open_vacancies = employer.get('open_vacancies')

            # тело sql запроса
            sql_query = (f"INSERT INTO employers (employer_name, employer_url, vacancies_url, open_vacancies) "
                         f"VALUES ('{employer_name}', '{employer_url}', '{vacancies_url}', '{open_vacancies}')")

            # выполняем запрос
            self.cursor.execute(sql_query)
            # коммитим запрос в бд.
            self.dbconnect.commit()

            employer_index += 1

            for vacancy in vacancies:
                # получаем данные из словаря employers.
                vacancy_name = vacancy.get('name')
                city = vacancy.get('area').get('name')
                employer_id = employer_index
                salary, currency = validate_salary(vacancy.get('salary'))
                publication_date = vacancy.get('published_at')
                vacancy_url = vacancy.get('alternate_url')
                # re.sub - заменяет все теги по типу <highlighttext>, replace - заменяет апострофы в тексте на пробелы.
                requirement = re.sub(r'<.*?>', '', vacancy.get('snippet').get('requirement')).replace("'", " ")
                responsibility = vacancy.get('snippet').get('responsibility')
                required_experience = vacancy.get('experience').get('name')

                # тело sql запроса
                sql_query = (
                    f"INSERT INTO vacancies (vacancy_name, city, employer_id, salary, currency, publication_date, "
                    f"vacancy_url, requirement, responsibility, required_experience) "
                    f"VALUES ('{vacancy_name}', '{city}', '{employer_id}', '{salary}', '{currency}', "
                    f"'{publication_date}', '{vacancy_url}', '{requirement}', '{responsibility}', '{required_experience}')")

                # выполняем запрос
                self.cursor.execute(sql_query)
                # коммитим запрос в бд.
                self.dbconnect.commit()

    def close_connection(self):
        self.cursor.close()
        self.dbconnect.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cursor.execute("SELECT employer_name, open_vacancies FROM employers")

        result = self.cursor.fetchall()
        for string in result:
            employer, open_vacancies = string
            print(f"Работодатель: {employer}, открытых вакансий: {open_vacancies}.")

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        self.cursor.execute("SELECT employer_name, vacancy_name, salary, currency, vacancy_url FROM vacancies "
                            "INNER JOIN employers USING(employer_id)")

        result = self.cursor.fetchall()
        for string in result:
            employer, vacancy_name, salary, currency, vac_url = string
            print(f"{employer}, {vacancy_name}, зарплата: {salary} {currency}, ссылка на вакансию: {vac_url}")

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям.
        Из подсчёта средней зарплаты убраны вакансии с зп = 0."""
        self.cursor.execute("SELECT AVG(salary) AS AVERAGE_SALARY FROM vacancies WHERE salary > 0")
        result = self.cursor.fetchall()
        avg_salary = round(result[0][0], 2)
        print(f"Средняя зарплата по выбранным вакансиям: {avg_salary}")

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cursor.execute(f"SELECT DISTINCT vacancy_name, salary, currency FROM vacancies WHERE salary > "
                            f"(SELECT AVG(salary) FROM vacancies) ORDER BY salary DESC")

        result = self.cursor.fetchall()
        for string in result:
            vacancy_name, salary, currency = string
            print(f"{vacancy_name}, зарплата: {salary} {currency}")

    def get_vacancies_with_keyword(self, keywords: list):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        # Форматирует ключевые слова в строку для sql запроса. Получается строка по типу: %word1% OR %word2%
        word_string = " OR ".join(f"%{word}%" for word in keywords)
        # тело sql запроса.
        query = f"""SELECT DISTINCT vacancy_name, requirement, responsibility FROM vacancies 
        WHERE requirement LIKE '{word_string}' or responsibility LIKE '{word_string}'"""
        # выполняем запрос.
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # выводим результат на экран.
        for string in result:
            vacancy_name, requirement, responsibility = string
            print(f"{vacancy_name}\nТребования: {requirement}\nОбязанности: {responsibility}\n--------------------")
