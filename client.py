import requests
import os
import json
import pprint
import random
import datetime

def pretty(json_data):
    return json.dumps(json_data, ensure_ascii = False, indent = 2)

def prettyprint(json_data):
    print(pretty(json_data))

def get_hh_values(num_pages, text = 'Python'):

    BASE_URL = 'https://api.hh.ru/'
    params = {
        'text': text,
        'search_field': ['name', 'description']
        }

    page = 0
    employer_dict = {}
    area_dict = {}
    vacancy_dict = {}
    applicant = []
    resume = []
    vacancy_resume_list = []

    names_request = requests.get('http://names.drycodes.com/200?nameOptions=presidents')
    names_list = names_request.json()
    count = 0

    while page < num_pages:
        
        #Request part
        params['page'] = page
        request = requests.get(os.path.join(BASE_URL, 'vacancies'), params = params)
        _json = request.json()
        

        #In case num_pages is greater, then available number of pages
        if int(_json.get('pages')) == page: break

        page = int(_json.get('page')) + 1

        #Looping through vacancies and saving neccessary info in dict
        vacancies = _json.get('items')
        for index, vacancy in enumerate(vacancies):

            employer = vacancy.get('employer')
            area = vacancy.get('area')
            created_at = vacancy.get('created_at')
            salary = vacancy.get('salary')

            #Creating new entries in employer and area dicts
            if employer.get('id'):
                employer_dict[employer.get('id')] = (employer.get('id'), f"'{employer.get('name')}'", area.get('id'))
                area_dict[area.get('id')] = (area.get('id'), f"'{area.get('name')}'")

                if count <= len(names_list) - 1:
                    applicant.append((str(count), f"'{names_list[count]}'", area.get('id')))
                    count+=1
                
                #Working with vacancy dict
                vacancy_dict[vacancy.get('id')] = {
                    'vacancy_id': vacancy.get('id'),
                    'employer_id': employer.get('id'),
                    'position_name': f"'{vacancy.get('name')}'",
                    'created_at': created_at,
                    'compensation_from': 'Null',
                    'compensation_to': 'Null',
                    'compensation_gross': 'Null',
                }
                if salary:
                    vacancy_dict[vacancy.get('id')]['compensation_from'] = str(salary.get('from')) if salary.get('from') else 'Null'
                    vacancy_dict[vacancy.get('id')]['compensation_to'] = str(salary.get('to')) if salary.get('to') else 'Null'
                    vacancy_dict[vacancy.get('id')]['compensation_gross'] = str(salary.get('gross')) if salary.get('gross') else 'Null'

        
    #Converting to tuple
    for index, vacancy in enumerate(vacancy_dict.keys()):

        items = vacancy_dict[vacancy]
        if index < len(names_list) - 1:
            resume.append((str(index), str(199-index), items.get('position_name')))

        connections = []
        for i in range(random.randint(5, 40)):
            connections.append(random.randint(0, 195))
        result = list(set(connections))
        for connection in result:
            created_at = (
                datetime.datetime.strptime(items.get('created_at'), '%Y-%m-%dT%H:%M:%S%z') +
                datetime.timedelta(hours = random.randrange(500))
            ).strftime('%Y-%m-%dT%H:%M:%S')
            vacancy_resume_list.append((vacancy, str(connection), f"'{created_at}'"))
        
        vacancy_dict[vacancy] = (
            vacancy,
            items.get('employer_id'),
            items.get('position_name'),
            items.get('compensation_from'),
            items.get('compensation_to'),
            items.get('compensation_gross'),
            f"'{items.get('created_at')}'"
        )

    return {
        'employer_dict': list(employer_dict.values()),
        'area_dict': list(area_dict.values()), 
        'vacancy_dict': list(vacancy_dict.values()),
        'resume_dict': resume,
        'applicant_dict': applicant,
        'vacancy_resume_list': vacancy_resume_list,
    }


