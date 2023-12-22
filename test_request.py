# import requests

# json_data = {
#     'vacancy': "Тренер в спортзале",
#     'salary': 10000,
#     'experience': 2,
#     'description': "Тренер в спортзале Тренер в спортзале Тренер в спортзале Тренер в спортзале"
# }

# r = requests.post('http://0.0.0.0:8080/get_vacancies/', json=json_data)

# print(f"Status Code: {r.status_code}, Response: {r.json()}")

import requests
from pprint import pprint

json_data = {
    'vacancy': "Тренер в спортзале",
    'salary': 10000,
    'experience': 2,
    'description': "Менеджер по продажам"
}

r = requests.post('http://0.0.0.0:8080/get_resumes/', json=json_data)

pprint(f"Status Code: {r.status_code}, Response: {r.json()}")
