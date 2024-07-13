from src.Db_Worker import DBManager
from src.HeadHunterAPI import HeadHunterAPI
from src.user_interactive import user_interactive


def main():
    # создание экземпляра класса для работы с бд.
    dbmanager = DBManager()

    # создание таблиц.
    dbmanager.create_tables()

    # создание экземпляра класса для работы с api hh.ru.
    hh_api = HeadHunterAPI()
    employers = hh_api.get_employers("Информационные технологии")
    vacancies = []
    for employer in employers:
        # получаем ссылку на все вакансии работодателя.
        vacancy_url = employer.get('vacancies_url')
        vacancies.extend(hh_api.get_vacancies_from_employer(vacancy_url, "Менеджер"))

    # выполняем запрос на добавление данных в таблицу.
    dbmanager.save_data_to_database(employers, vacancies)

    # работа с пользователем.
    user_interactive()

    # удаление таблиц.
    dbmanager.drop_tables()

    # закрываем соединение с бд.
    dbmanager.close_connection()


if __name__ == "__main__":
    main()
