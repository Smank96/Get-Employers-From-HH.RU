def validate_salary(salary: dict) -> tuple[int, str]:
    """Функция для проверки указана ли зарплата.
    Возвращает кортеж из двух значений: зарплата и курс валюты."""
    if salary and salary.get('from'):
        salary_currency = (int(salary.get('from')), salary.get('currency'))
        return salary_currency
    else:
        salary_currency = (0, '')
        return salary_currency
