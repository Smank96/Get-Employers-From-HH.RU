from src.Db_Worker import DBManager
from src.HeadHunterAPI import HeadHunterAPI
from src.user_interactive import user_interactive


def main():
    # создание экземпляра класса для работы с бд.
    dbmanager = DBManager()

    # создаем экземпляр класса для работы с api hh.ru.
    hh_api = HeadHunterAPI()
    emp_list = hh_api.get_employers("Информационные технологии")
    vac_list = []
    for emp in emp_list:
        # получаем ссылку на вакансии работодателя из словаря
        vacancy_url = emp.get('vacancies_url')
        vac_list.extend(hh_api.get_vacancies_from_employer(vacancy_url, "Менеджер"))

    # выполняем запрос на добавление данных в таблицу.
    dbmanager.save_data_to_database(emp_list, vac_list)
    # закрываем соединение с бд.
    dbmanager.close_connection()

    user_interactive()


if __name__ == "__main__":
    main()
