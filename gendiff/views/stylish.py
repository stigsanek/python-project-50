from collections import OrderedDict

from gendiff import diff


def get_item_value(value, indent: int) -> str:
    """
    Get string data for item value

    :param value: value
    :param indent: indent
    :return: str
    """
    if isinstance(value, dict):
        ind = "  " * indent
        end_bracket = "  " * (indent - 1)
        temp = []
        for k, v in value.items():
            if isinstance(v, dict):
                temp.append(f"{ind}  {k}: {get_item_value(v, indent + 2)}\n")
            else:
                temp.append(f"{ind}  {k}: {v}\n")
        return "{\n" + f"{''.join(temp)}{end_bracket}" + "}"

    if isinstance(value, bool):
        return str(value).lower()

    if value is None:
        return "null"

    return value


def get_all_values(data: OrderedDict, depth: int = 1) -> list:
    """
    Get list for all data

    :param data: diff data
    :param depth: default depth
    :return: list
    """
    temp = []
    ind = "  " * depth
    inner_depth = depth + 2

    for k, v in data.items():
        status = diff.get_status(diff=data, key=k)
        values = diff.get_values(diff=data, key=k)

        if status == diff.NESTED:
            temp.append(f"{ind}  {k}: " + "{\n")
            temp += get_all_values(values[0], inner_depth)
            temp.append(f"{ind}  " + "}\n")
        if status == diff.CHANGED:
            before = f"{ind}- {k}: {get_item_value(values[0], inner_depth)}\n"
            after = f"{ind}+ {k}: {get_item_value(values[1], inner_depth)}\n"
            temp.append(before + after)
        if status == diff.UNCHANGED:
            value = get_item_value(values[0], inner_depth)
            temp.append(f"{ind}  {k}: {value}\n")
        if status == diff.ADDED:
            value = get_item_value(values[0], inner_depth)
            temp.append(f"{ind}+ {k}: {value}\n")
        if status == diff.DELETED:
            value = get_item_value(values[0], inner_depth)
            temp.append(f"{ind}- {k}: {value}\n")

    return temp


def render(data: OrderedDict) -> str:
    """
    Get diff representation string

    :param data: diff data
    :return: str
    """
    return "{\n" + f"{''.join(get_all_values(data))}" + "}"