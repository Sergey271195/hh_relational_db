def insert_into(output, table_name, values, schema = None, fields = None):
    output.write('INSERT INTO')
    output.write(f' {schema}.{table_name}') if schema else (f' {table_name}')
    if fields:
        output.write('(' +', '.join(fields) + ')')
    output.write('\nVALUES ' + '(' + ', '.join(values[0]) + ')')
    if len(values) > 1:
        for value in values[1:]:
            joined = '(' + ', '.join(value) + ')'
            output.write(',\n' + ' '*7 + joined)
    output.write(';\n')

def create_table(output, table_name, fields, schema = None, constraints = None):
    output.write(f'CREATE TABLE {schema}.{table_name} (\n') if schema else output.write(f'CREATE TABLE {table_name} (\n')
    max_length = len(max(fields.keys(), key = len))
    indent = '    '
    rows = []
    for key in list(fields.keys())[:-1]:
        output.write(indent + key.ljust(max_length))
        output.write(indent + fields.get(key) + ',\n')
    
    last_key = list(fields.keys())[-1]
    output.write(indent + last_key.ljust(max_length))
    output.write(indent + fields.get(last_key))
    if constraints:
        output.write(',\n')
        for constrain in constraints[:-1]:
            output.write(indent + constrain + ',\n')
        last_constraint = constraints[-1]
        output.write(indent + last_constraint + '\n')
    else:
        output.write('\n')
    output.write(');\n')



