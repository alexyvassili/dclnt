import os
import importlib
from git import Repo, exc
from tempfile import mkdtemp

# Filewalker tries to get filenames from the suggested path
# If it can't: we return empty list


def get_file_names(path: str, proj_name='') -> list:
    names = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            names.append(os.path.join(dirname, file))
    names = [f for f in names if f.endswith('py')]
    print('Total {} .py files in {} project.'.format(len(names), proj_name))
    return names


def get_file_names_from_py_module(dir_name: str) -> list:
    try:
        path = os.path.dirname(importlib.util.find_spec(dir_name).origin)
    except AttributeError:
        print("Error: Module '{}' is not found.".format(dir_name))
        return []
    except ModuleNotFoundError:
        print("Error: Location of '{}' is not found.".format(dir_name))
        return []
    else:
        return get_file_names(path, dir_name)


def get_file_names_from_git_repo(url):
    project_name = url.split('/')[-1]
    # creating directory in %TEMP% folder for clone git repo
    repo_dir = mkdtemp(suffix=None, prefix=(project_name+'.'), dir=None)
    print('Getting resource: {} ...'.format(url))
    try:
        Repo.clone_from(url, repo_dir)
    except exc.GitCommandError as git_err:
        print('GitHub error: ', git_err.stderr)
        return []
    else:
        return get_file_names(repo_dir, project_name)
