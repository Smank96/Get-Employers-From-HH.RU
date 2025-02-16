from src.Db_Worker import DBManager


def user_interactive():
    """Функция для взаимодействия с пользователем."""
    print("Введите 1 для получения списка компаний и кол-ва вакансий.")
    print(f"Введите 2 для получения списка вакансий с полями: "
          f"название компании, название вакансии, зарплата, ссылка на вакансию.")
    print("Введите 3 для получения средней зарплаты по вакансиям.")
    print("Введите 4 для получения списка вакансий с зарплатой выше средней по всем вакансиям.")
    print("Введите 5 для получения списка отфильтрованного вакансий по ключевым словам.")

    dbmanager = DBManager()

    user_action = int(input())

    if user_action == 1:
        dbmanager.get_companies_and_vacancies_count()
    elif user_action == 2:
        dbmanager.get_all_vacancies()
    elif user_action == 3:
        dbmanager.get_avg_salary()
    elif user_action == 4:
        dbmanager.get_vacancies_with_higher_salary()
    elif user_action == 5:
        keyword = input("Введите ключевые слова для фильтрации вакансий: ").lower().split()
        dbmanager.get_vacancies_with_keyword(keyword)
    else:
        print("Введено некорректное значение.")

    # закрываем соединение с бд.
    dbmanager.close_connection()
