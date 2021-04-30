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
            ' --toc'
            ' --toc-depth 3'
            ' -V toc-title="Table of Contents" -s ') + ' '.join(paths)

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
                paths.append(focus+'.md')

            # if metrics is not None:
            #     text = get_fa_table(values['wg-name'] + '/focus-areas/' + focus + '/README.md')
            #     print(text, type(text))

            #     gen_md_file(focus, 2, text)

            for metric in metrics:
                # gen_md_file(metric, 3)    # no need for metrics heading
                paths.append(values['wg-name'] + '/focus-areas/' + focus + '/' + metric)
        except:
            continue
    pprint(paths)
    # return paths


def gen_md_file(name, level, text):

    # if name[len(name)-3:] != '.md':
    #     name += '.md'

    stuff = '#'*level + ' ' + name.upper() + '\n\n' + text
    name += '.md'

    print("Generating file '{}' with text '{}'".format(name, stuff))


    with open(name, 'w') as f:
        f.write(stuff)

    paths.append(name)


def decrease_level(paths):

    print("\nDecreasing heading levels by 2 in metric markdowns")

    for i in paths:
        if '/' in i:
            cmd = 'sed -i "s/^\#/###/g" ' + i
            os.system(cmd)


def get_fa_table(file_path):
    
    cmd = "sed 's/[][]\|([^()]*)//g' " + file_path
    return subprocess.check_output(cmd, shell=True).decode("utf-8")


def get_lorem_ipsum():
    return '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''


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
print("Bringing side scripts...")

os.chdir('test-env')
os.system('rm -rf *')
os.mkdir('images')
os.system('cp ../side-scripts/* .')

paths = []

# Download and generate focus-areas markdowns
for key, values in data['focus-areas'].items():
    
    print('Downloading', key)
    cmd = 'wget ' + values
    os.system(cmd)

    subprocess.check_call(['./get_focus_areas.sh', key])

# delete this from the dict
del data['focus-areas']


for key, values in data.items():

    if values['include-wg-flag']:

        print("\nCloning '{}' from '{}' branch\n".format(key, values['github-branch']))
        subprocess.check_call(['git', 'clone', '-b', values['github-branch'], values['github-link'], key])

        gen_md_file(values['wg-name'], 1, get_lorem_ipsum())

        # paths =
        generate_paths(values, paths)

    else:
        print('[WARNING]: Flag off for {}, ignoring this WG'.format(key))

decrease_level(paths)

generate_PDF(paths)

