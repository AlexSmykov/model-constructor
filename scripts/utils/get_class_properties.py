import inspect


def get_class_properties(class_interface: any) -> list[str]:
    return list(filter(__check_item_is_custom_field, map(__get_key, inspect.getmembers(class_interface))))


def __get_key(item: (str, any)) -> str:
    return item[0]


def __check_item_is_custom_field(item: str) -> bool:
    if (item[0] == '_' and item[1] == '_') or item == 'name' or item == 'value':
        return False
    return True
