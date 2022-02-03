def filtering(data_list, filters, or_mode=False):
    new_list = []
    for filtr in filters:
        op = filtr.get('op')

        if op == 'equal':
            new_list = (new_list if or_mode else []) + [d for d in data_list if str(d.__dict__[filtr.get('field')]).lower() == str(filtr.get('value')).lower()]
        elif op == '>':
            new_list = (new_list if or_mode else []) + [d for d in data_list if int(d.__dict__[filtr.get('field')]) > int(filtr.get('value'))]
        elif op == '<':
            new_list = (new_list if or_mode else []) + [d for d in data_list if int(d.__dict__[filtr.get('field')]) < int(filtr.get('value'))]
        elif op == '>=':
            new_list = (new_list if or_mode else []) + [d for d in data_list if int(d.__dict__[filtr.get('field')]) >= int(filtr.get('value'))]
        elif op == '<=':
            new_list = (new_list if or_mode else []) + [d for d in data_list if int(d.__dict__[filtr.get('field')]) <= int(filtr.get('value'))]
        elif op == 'contains':
            new_list = (new_list if or_mode else []) + [d for d in data_list if str(filtr.get('value')).lower() in str(d.__dict__[filtr.get('field')]).lower()]
        if not or_mode:
            data_list = new_list
    return list(set(new_list))
