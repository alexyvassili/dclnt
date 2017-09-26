import ast


def filter_funcs(node) -> bool:
    """Filter to get functions names and remove dunder names"""
    if not isinstance(node, ast.FunctionDef):
        return False
    elif node.name.startswith('__') or node.name.endswith('__'):
        return False
    else:
        return True


def filter_vars(node):
    """Filter to get variables names"""
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        return True
    # elif node.name.startswith('__') or node.name.endswith('__'):
    #     return False
    else:
        return False


def get_func_names(tree) -> list:
    names = [node.name.lower() for node in ast.walk(tree) if filter_funcs(node)]
    return names


def get_var_names(tree) -> list:
    names = [node.targets[0].id.lower() for node in ast.walk(tree) if filter_vars(node)]
    return names


def get_all_func_names(trees):
    names = [name for tree in trees for name in get_func_names(tree)]
    print('{} names found.'.format(len(names)))
    return names


def get_all_var_names(trees):
    names = [name for tree in trees for name in get_var_names(tree)]
    print('{} names found.'.format(len(names)))
    return names
