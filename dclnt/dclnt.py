import ast
import os
import importlib
import collections
import nltk
from nltk import pos_tag
import function_pipe as fpn


try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


@fpn.FunctionNode  # decorator for organize function pipe
def get_file_names_from_module(module: str) -> list:
    names = []
    try:
        path = os.path.dirname(importlib.util.find_spec(module).origin)
    except AttributeError:
        print("Error: Module '{}' is not found.".format(module))
        return names
    else:
        for dirname, dirs, files in os.walk(path, topdown=True):
            for file in files:
                names.append(os.path.join(dirname, file))
        # TODO: here we can set names limit on 100 as is in source file
        names = [f for f in names if f.endswith('py')]
        print('Total {} .py files in {} module.'.format(len(names), module))
        return names


def get_tree(file, with_file_name=False, with_file_content=False) -> tuple:
    with open(file, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as e:
        print(e)
        # TODO: i can't understand how catch None result
        tree = None
    finally:
        tree_list = [tree]
        if with_file_name:
            tree_list.append(file)
        if with_file_content:
            tree_list.append(main_file_content)
        return tuple(tree_list)

@fpn.FunctionNode
def generate_trees(file_names: list, with_file_name=False, with_file_content=False) -> list:
    trees = []
    for f in file_names:
        tree = get_tree(f, with_file_name=with_file_name, with_file_content=with_file_content)
        if tree[0]:
            trees.append(tree)
    print('{} trees generated.'.format(len(trees)))
    return trees


def filter_nodes(node) -> bool:
    """Filter to get functions names and remove dunder names"""
    if not isinstance(node, ast.FunctionDef):
        return False
    elif node.name.startswith('__') or node.name.endswith('__'):
        return False
    else:
        return True


def get_func_names(tree) -> list:
    names = [node.name.lower() for node in ast.walk(tree) if filter_nodes(node)]
    return names

@fpn.FunctionNode
def get_all_func_names(trees):
    return [name for tree in trees for name in get_func_names(tree[0])]

@fpn.FunctionNode
def get_words_from_func_names(names):
    words = []
    for func_name in names:
        words += func_name.split('_')
    # TODO: sometimes split get empty strings
    return list(filter(bool, words))

@fpn.FunctionNode
def get_verbs_from_words(words) -> list:
    # TODO: strange behavior of NLTK: verb tag on non-verb words
    return [item[0] for item in pos_tag(words) if item[1][:2] == 'VB']

@fpn.FunctionNode
def get_top_words(words, top_size=10) -> 'collections.Counter list':
    return collections.Counter(words).most_common(top_size)


def get_top_verbs_in_func_names(module: str, top_size=10) -> list:
    """Organize function pipe for getting top verbs in module"""
    pipe = (get_file_names_from_module
            >> generate_trees
            >> get_all_func_names
            >> get_words_from_func_names
            >> get_verbs_from_words
            >> get_top_words.partial(top_size=top_size)) # .partial allows to add kwarguments to a func
    return pipe(module)

def example():
    words = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    for project in projects:
        verbs = get_top_verbs_in_func_names(project, top_size=12)
        words += verbs
    words = [i[0] for i in words]
    print('total {} words, {} unique'.format(len(words), len(set(words))))
    top_size = 10
    for word, occurrence in collections.Counter(words).most_common(top_size):
        print(word, occurrence)

if __name__ == '__main__':
    example()