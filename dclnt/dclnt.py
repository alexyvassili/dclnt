#!/usr/bin/python3
import function_pipe as fpn
import argparse
import os

# DCLNT implements function pipe for gathering statistic from py files: words (verbs, nouns)
# in functions/variables names. This is 7 stages pipe scheme:

import filewalkers
import parsers
import getnames
import words
import statistic
import outs


def createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--names', default='funcs', choices=['funcs', 'vars'],
                        help='type of names: "vars" for variables | "funcs" for functions (default)')
    parser.add_argument('-p', '--pof', default='all', choices=['verb', 'noun', 'all'],
                        help='type of part of speech searching: "verb", "noun" or "all" (default)')
    parser.add_argument('-t', '--top', type=int, default=10,
                        help='top size, default=10')
    parser.add_argument('-O', '--out', default='stdout',
                        help='output form, default="stdout" '
                             'for console output, you can specify .csv '
                             'or .json file for output in appropriate format')
    parser.add_argument('url')

    return parser

parser = createParser()
namespace = parser.parse_args()
PRINTLINE = {} # used for print information at run time

# 1st Stage: setting file walker: github, user directory or python module
# we search github in url, if not - we search directory in filesystem,
# if not - we suppose that it is python module
URL = namespace.url
if 'github.com' in URL.lower():
    fileWalker = fpn.FunctionNode(filewalkers.get_file_names_from_git_repo)
elif os.path.exists(URL):
    URL = os.path.realpath(URL)
    fileWalker = fpn.FunctionNode(filewalkers.get_file_names)
else:
    fileWalker = fpn.FunctionNode(filewalkers.get_file_names_from_py_module)

PRINTLINE['project'] = URL

# 2nd Stage: setting tree parser for files: ast parser is used
treesGenerator = fpn.FunctionNode(parsers.generate_trees)

# 3rd Stage: setting name filter: for functions only, variables only
if namespace.names == 'funcs':
    PRINTLINE['names'] = 'functions'
    namesGetter = fpn.FunctionNode(getnames.get_all_func_names)
elif namespace.names == 'vars':
    PRINTLINE['names'] = 'variables'
    namesGetter = fpn.FunctionNode(getnames.get_all_var_names)

# 4th Stage: setting word from names function, filter dunder names
wordsGetter = fpn.FunctionNode(words.get_words_from_names)

# 5th Stage: specify part of speech from all words
if namespace.pof == 'verb':
    PRINTLINE['pof'] = 'verbs'
    POF_TAG = 'VB'
elif namespace.pof == 'noun':
    PRINTLINE['pof'] = 'nouns'
    POF_TAG = 'NN'
elif namespace.pof == 'all':
    PRINTLINE['pof'] = 'all words'
    POF_TAG = 'ALL'
partsOfSpeechGetter = fpn.FunctionNode(words.get_pof_from_words)

# 6th Stage: setting statistic engine: top words counter
TOP_SIZE = namespace.top
PRINTLINE['topsize'] = TOP_SIZE
topGetter = fpn.FunctionNode(statistic.get_top_words)

# 7th Stage: specify type of output: console, json or csv
FILE = namespace.out
if FILE == 'stdout':
    PRINTLINE['out'] = 'stdout'
    output = fpn.FunctionNode(outs.console_or_file_out)
elif FILE[-3:] == 'csv':
    PRINTLINE['out'] = FILE
    output = fpn.FunctionNode(outs.csv_out)
elif FILE[-4:] == 'json':
    PRINTLINE['out'] = FILE
    output = fpn.FunctionNode(outs.json_out)
else:
    print('\033[1m' + 'WARNING: .json or .csv file extension was not found in output filename:'
          ' writing plain text output.' + '\033[0m')
    PRINTLINE['out'] = FILE
    output = fpn.FunctionNode(outs.console_or_file_out)



def processing_pipe(project: str) -> 'pipe':
    """Organize function pipe for getting top verbs in module"""
    pipe = (fileWalker
            >> treesGenerator
            >> namesGetter
            >> wordsGetter
            # .partial allows to add arguments to a function in pipe
            >> partsOfSpeechGetter.partial(pof_tag=POF_TAG)
            >> topGetter.partial(top_size=TOP_SIZE)
            >> output.partial(file=FILE))
    return pipe(project)


def example():
    # TODO: Now you can not just import this package, it's tied to command-line arguments
    processing_pipe('flask')


if __name__ == '__main__':
    print('Processing {} project for top {} {} in {} names with output to {}...'.format(
        PRINTLINE['project'],
        PRINTLINE['topsize'],
        PRINTLINE['pof'],
        PRINTLINE['names'],
        PRINTLINE['out']))
    processing_pipe(URL)