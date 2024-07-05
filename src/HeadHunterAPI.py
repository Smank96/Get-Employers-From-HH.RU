import requests


class HeadHunterAPI:
    """Класс для взаимодействия с API HH.RU"""

    def __init__(self):
        self.url = ""
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {}
        self.employers = []
        self.vacancies = []

    def get_employers(self, keyword: str) -> list[dict]:
        """Подключается к api hh.ru и получает работодателей по ключевому слову."""
        self.url = 'https://api.hh.ru/employers'
        self.params = {'text': keyword, 'page': 0, 'per_page': 10, 'only_with_vacancies': True}

        while self.params.get('page') != 1:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            employers = response.json()['items']
            self.employers.extend(employers)
            self.params['page'] += 1

        return self.employers

    def get_vacancies_from_employer(self, vacancy_url: str, keyword: str) -> list[dict]:
        self.url = vacancy_url
        self.params = {'text': keyword, 'page': 0, 'per_page': 100}

        while self.params.get('page') != 10:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

        return self.vacancies
