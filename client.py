import requests
import os
import json

def pretty(json_data):
    return json.dumps(json_data, ensure_ascii = False, indent = 2)

def prettyprint(json_data):
    print(pretty(json_data))

BASE_URL = 'https://api.hh.ru/'
params = {'text': 'Python', 'search_field': ['name', 'description']}

#Suggested names for vacancies search
##'id': '1.221', 'name': 'Программирование, Разработка', 'laboring': False
""" request = requests.get(
    os.path.join(BASE_URL, 'suggests/vacancy_search_keyword'), params = params) """

""" request = requests.get(
    os.path.join(BASE_URL, 'specializations')) """

#request = requests.get(os.path.join(BASE_URL, 'dictionaries'))

necessary_fields = ['salary', 'name', 'area', 'employer', 'created_at']
# if salary != null  ['salary.from', 'salary.to', 'salary.gross']
# if area != null 'area.name'
# if employer != null 'employer.name'

# randomly generate response_counter
# randomly generate first_response_at
#ORDER BY multiple times LIMIT = 5


vacancies_without_salary = []
page = 0
while len(vacancies_without_salary) < 20:
    params['page'] = page
    request = requests.get(os.path.join(BASE_URL, 'vacancies'), params = params)
    _json = request.json()
    page = int(_json.get('page')) + 1
    print(f'Page {page}')
    vacancies = _json.get('items')
    for vacancy in vacancies:
        if vacancy.get('salary'):
            print(f'__________VACANCY {len(vacancies_without_salary)}____________')
            vacancies_without_salary.append(vacancy)

prettyprint(_json)

""" prettyprint(_json.get('vacancy_search_fields'))
prettyprint(_json.get('vacancy_label'))
for key in _json.keys():
    print(key) """