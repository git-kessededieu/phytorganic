from ast import literal_eval


def str_to_json(string = ""):
    if len(string) > 1:
        return literal_eval(string)
    else:
        return {}
