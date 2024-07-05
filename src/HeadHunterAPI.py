import requests


class HeadHunterAPI:
    """Класс для взаимодействия с API HH.RU"""

    def __init__(self):
        self.url = 'https://api.hh.ru/employers'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 10, 'only_with_vacancies': True}
        self.employers = []

    def get_employers(self, keyword: str) -> list[dict]:
        """Подключается к api hh.ru и получает работодателей по ключевому слову."""
        self.params['text'] = keyword

        while self.params.get('page') != 2:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            employers = response.json()['items']
            self.employers.extend(employers)
            self.params['page'] += 1

        return self.employers
