def obj_to_dict(instance, fields=None, exclude=None):
    """transfer a obj to a dict.
    :param instance: an instance of model
    :param fields: fields need to transfer
    :param exclude: fields not need to transfer
    :param decode_list: fields need to decode
    :returns: dict
    """
    concrete_fields = instance.__mapper__.c.keys()
    data = {}
    for f in concrete_fields:
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f] = getattr(instance, f)
    return data


def obj_list_to_list_dict(obj_list, fields=None, exclude=None):
    """transfer objs to a list.
    :param obj_list: many instance set of model
    :param fields: fields need to transfer
    :param exclude: fields not need to transfer
    :param decode_list: fields need to decode
    :returns: dict
    """
    obj_dict_list = []
    for obj in obj_list:
        concrete_fields = obj.__mapper__.c.keys()
        data = {}
        for f in concrete_fields:
            if fields and f not in fields:
                continue
            if exclude and f in exclude:
                continue
            data[f] = getattr(obj, f)
        obj_dict_list.append(data)
    return obj_dict_list