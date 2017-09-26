import ast


def get_tree(file) -> tuple:
    with open(file, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        print(e)
        tree = None
    finally:
        return tree


def generate_trees(file_names: list) -> list:
    trees = []
    for f in file_names:
        tree = get_tree(f)
        if tree:
            trees.append(tree)
    print('{} trees generated.'.format(len(trees)))
    return trees
