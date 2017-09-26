import json
import csv
import sys


def console_or_file_out(words: tuple, file):
    if file == 'stdout':
        file = sys.stdout
    else:
        file = open(file, 'w')
        print('Saving to {}.'.format(file.name))
    print('  Here is the words top: ', file=file)
    i = 1
    for word in words:
        print('{:3} : {:10}: {:2}'.format(i, word[0], word[1]), file=file)
        i += 1
    if not file == sys.stdout:
        file.close()


def json_out(words: tuple, file):
    with open(file, 'w') as outfile:
        json.dump(dict(words), outfile, indent=4)
        print('\n', file=outfile)
        print('{} created.'.format(file))


def csv_out(words: tuple, file):
    with open(file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(words)
        print('{} created.'.format(file))

