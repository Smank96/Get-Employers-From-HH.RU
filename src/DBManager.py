import re
import psycopg2
from src.read_config import read_config
# from src.utils import validate_salary


class DBManager:
    def __init__(self):
        params = read_config()

        self.dbconnect = psycopg2.connect(dbname=params.get('dbname'),
                                          host=params.get('host'),
                                          user=params.get('user'),
                                          password=params.get('password'),
                                          port=params.get('port'))

        self.cursor = self.dbconnect.cursor()

        print("Подключение к базе установленно.")

    def save_data_to_database(self, employers: list[dict], vacancies: list[dict]):
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
                requirement = re.sub(r'<.*?>', '', vacancy.get('snippet').get('requirement')).replace("'a", " ")
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
        print("Подключение к базе завершено.")

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cursor.execute("SELECT employer_name, open_vacancies FROM employers")
        print(self.cursor.fetchall())

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        self.cursor.execute("SELECT employer_name, vacancy_name, salary, vacancy_url FROM vacancies "
                            "INNER JOIN employers USING(employer_id)")
        print(self.cursor.fetchall())

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.cursor.execute("SELECT AVG(salary) AS AVERAGE_SALARY FROM vacancies")
        print(self.cursor.fetchall())

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self, keywords: list):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass
