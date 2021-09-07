def filtering(data_list, filters):
    for filtr in filters:
        op = filtr.get('op')
        if op == 'equal':
            data_list = [d for d in data_list if str(d.__dict__[filtr.get('field')]).lower() == str(filtr.get('value')).lower()]
        elif op == '>':
            data_list = [d for d in data_list if int(d.__dict__[filtr.get('field')]) > int(filtr.get('value'))]
        elif op == '<':
            data_list = [d for d in data_list if int(d.__dict__[filtr.get('field')]) < int(filtr.get('value'))]
        elif op == '>=':
            data_list = [d for d in data_list if int(d.__dict__[filtr.get('field')]) >= int(filtr.get('value'))]
        elif op == '<=':
            data_list = [d for d in data_list if int(d.__dict__[filtr.get('field')]) <= int(filtr.get('value'))]
        elif op == 'contains':
            data_list = [d for d in data_list if str(filtr.get('value')).lower() in str(d.__dict__[filtr.get('field')]).lower()]
    return data_list
