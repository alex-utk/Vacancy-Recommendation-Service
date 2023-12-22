import requests

json_data = {
    'vacancy': "Тренер в спортзале",
    'salary': 10000,
    'experience': 2,
    'description': "Тренер в спортзале Тренер в спортзале Тренер в спортзале Тренер в спортзале",
    'city_name': 'Москва'
}

r = requests.post('http://0.0.0.0:8080/get_vacancies/', json=json_data)

print(f"Status Code: {r.status_code}, Response: {r.json()}")




json_data = {
    'vacancy': "Тренер в спортзале",
    'salary': 10000,
    'experience': 2,
    'description': "Менеджер по продажам",
    'city_name': 'Москва'
}

r = requests.post('http://0.0.0.0:8080/get_resumes/', json=json_data)

print(f"Status Code: {r.status_code}, Response: {r.json()}")
