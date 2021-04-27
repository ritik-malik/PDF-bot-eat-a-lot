# This is the main py script to generate automated PDF from metrics
# It takes a YML file as an input (command line arg)
#
# THE SCRIPT IS NOT CLEAN RIGHT NOW! (for testing purposes only)
#
# Usage: python3 PDF-bot.py conf.yml

import yaml
import os
import subprocess
from sys import argv, exit
from pprint import pprint

def generate_PDF(paths):

    print("\nGenerating the PDF now...\n")
    os.system('cp ../side-scripts/* .')
    
    cmd = ('pandoc -f gfm'
            ' -H template.tex'
            ' -o output.pdf'
            ' --pdf-engine xelatex'
            ' -V mainfont="DejaVu Serif"'
            ' -V monofont="DejaVu Sans Mono"'
            ' -V linkcolor:blue'
            ' -V fontsize=12pt'
            ' --include-before-body cover.tex'
            ' --highlight-style pygments.theme'
            ' --toc -s ') + ' '.join(paths)

    # print(cmd)
    os.system(cmd)
    os.system('cp output.pdf ..')

    print("Generated the PDF!\n")


def generate_paths(values, paths):

    print("\nGenerating relative paths...\n")

    for focus, metrics in values['focus-areas'].items():
        
        try:

            cmd = 'cp ' + values['wg-name'] + '/focus-areas/' + focus + '/images/* images'
            os.system(cmd)

            if metrics is not None:
                gen_md_file(focus, 2)

            for metric in metrics:
                # gen_md_file(metric, 3)    # no need for metrics heading
                paths.append(values['wg-name'] + '/focus-areas/' + focus + '/' + metric)
        except:
            continue
    pprint(paths)
    # return paths


def gen_md_file(name, level):

    # if name[len(name)-3:] != '.md':
    #     name += '.md'

    text = '#'*level + ' ' + name.upper()
    name += '.md'

    print("Generating file '{}' with text '{}'".format(name, text))


    with open(name, 'w') as f:
        f.write(text)

    paths.append(name)


def decrease_level(paths):

    print("\nDecreasing heading levels by 2 in metric markdowns")

    for i in paths:
        if '/' in i:
            cmd = 'sed -i "s/^\#/###/g" ' + i
            os.system(cmd)



###### main()

print("\n------------------------------")
print("<===WELCOME TO PY PDF BOT ===>")
print("------------------------------\n")

# read YML config file
try:
    with open(argv[1]) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
except:
    print("\nUsage: python3 PDF-bot.py conf.yml\n")
    exit(1)

print("YML file structure: \n")
pprint(data)

print("\nMoving to test-env dir...")
print("Removing files and folders [if any]...")

os.chdir('test-env')
os.system('rm -rf *')
os.mkdir('images')

paths = []

for key, values in data.items():

    if values['include-wg-flag']:

        print("\nCloning '{}' from '{}' branch\n".format(key, values['github-branch']))
        subprocess.check_call(['git', 'clone', '-b', values['github-branch'], values['github-link'], key])

        gen_md_file(values['wg-name'], 1)

        # paths =
        generate_paths(values, paths)

    else:
        print('[WARNING]: Flag off for {}, ignoring this WG'.format(key))

decrease_level(paths)

generate_PDF(paths)

