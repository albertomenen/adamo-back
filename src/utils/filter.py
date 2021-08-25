def filtering(data_list, filters):
    for filtr in filters:
        op = filtr.get('op')
        if op == 'equal':
            data_list = [d for d in data_list if d.__dict__[filtr.get('field')] == filtr.get('value')]
        elif op == '>':
            data_list = [d for d in data_list if d.__dict__[filtr.get('field')] > int(filtr.get('value'))]
        elif op == '<':
            data_list = [d for d in data_list if d.__dict__[filtr.get('field')] < int(filtr.get('value'))]
        elif op == '>=':
            data_list = [d for d in data_list if d.__dict__[filtr.get('field')] >= int(filtr.get('value'))]
        elif op == '<=':
            data_list = [d for d in data_list if d.__dict__[filtr.get('field')] <= int(filtr.get('value'))]
        elif op == 'contains':
            data_list = [d for d in data_list if filtr.get('value') in d.__dict__[filtr.get('field')]]
    return data_list
