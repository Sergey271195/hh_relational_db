from sql_gen import create_table, insert_into
from client import get_hh_values

SCHEMA = 'homework'

with open('test.sql', 'w') as f:

    create_table(
        schema = SCHEMA,
        output = f,
        table_name = 'area',
        fields = {
            'area_id': 'integer PRIMARY KEY',
            'area_name': 'text NOT NULL',
        })

    create_table(
        schema = SCHEMA,
        output = f,
        table_name = 'employer',
        fields = {
            'employer_id': 'SERIAL PRIMARY KEY',
            'employer_name': 'text NOT NULL',
            'area_id':  f'integer NOT NULL REFERENCES {SCHEMA}.area (area_id) ON DELETE CASCADE',
        })
    
    create_table(
        schema = SCHEMA,
        output = f,
        table_name = 'vacancy',
        fields = {
            'vacancy_id': 'SERIAL PRIMARY KEY',
            'employer_id': f'integer NOT NULL REFERENCES {SCHEMA}.employer (employer_id) ON DELETE CASCADE',
            'position_name': 'text NOT NULL',
            'compensation_from': 'integer',
            'compensation_to': 'integer',
            'compensation_gross': 'boolean',
            'created_at': 'timestamp DEFAULT now()',
            'responses': 'integer DEFAULT 0',
            'first_response_at': 'timestamp',
        }
    )

    create_table(
        schema = SCHEMA,
        output = f,
        table_name = 'applicant',
        fields = {
            'applicant_id': 'SERIAL PRIMARY KEY',
            'applicant_name': 'text NOT NULL',
            'area_id': f'integer REFERENCES {SCHEMA}.area (area_id) ON DELETE SET NULL'
        }
    )

    create_table(
        schema = SCHEMA,
        output = f,
        table_name = 'resume',
        fields = {
            'resume_id': 'SERIAL PRIMARY KEY',
            'applicant_id': f'integer NOT NULL REFERENCES {SCHEMA}.applicant (applicant_id) ON DELETE CASCADE',
            'position_objective': 'text',
        }
    )

    create_table(
        schema = SCHEMA,
        output = f,
        table_name = 'vacancy_resume',
        fields = {
            'relation_id': 'SERIAL PRIMARY KEY',
            'vacancy_id': f'integer NOT NULL REFERENCES {SCHEMA}.vacancy (vacancy_id) ON DELETE CASCADE',
            'resume_id': f'integer NOT NULL REFERENCES {SCHEMA}.resume (resume_id) ON DELETE CASCADE',
            'created_at': 'timestamp DEFAULT now()',
        },
        constraints = ['CONSTRAINT unique_relations UNIQUE(vacancy_id, resume_id)'],
    )

dicts = get_hh_values(25, 'python')

with open('test2.sql', 'w', encoding = 'utf-16') as f:

    insert_into(
        output = f,
        table_name = 'area',
        values = dicts.get('area_dict'),
        schema = SCHEMA,
    )

    insert_into(
        output = f,
        table_name = 'employer',
        values = dicts.get('employer_dict'),
        schema = SCHEMA,
    )

    insert_into(
        output = f,
        table_name = 'vacancy',
        values = dicts.get('vacancy_dict'),
        schema = SCHEMA,
    )


    insert_into(
        output = f,
        table_name = 'applicant',
        values = dicts.get('applicant_dict'),
        schema = SCHEMA,
    )

    insert_into(
        output = f,
        table_name = 'resume',
        values = dicts.get('resume_dict'),
        schema = SCHEMA,
    )