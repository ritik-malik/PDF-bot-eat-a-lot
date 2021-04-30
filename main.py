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
import helper

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

    print("\nGenerating relative paths to the metric markdowns...\n")

    for focus, metrics in values['focus-areas'].items():
        
        # try:
        cmd = 'cp ' + values['wg-name'] + '/focus-areas/' + focus + '/images/* images'
        os.system(cmd)

        # add focus-areas markdown
        if metrics is not None:
            paths.append(focus+'.md')

            # add metrics markdown
            for metric in metrics:
                paths.append(values['wg-name'] + '/focus-areas/' + focus + '/' + metric)
        # except:
        #     continue
    
    pprint(paths)
    return paths


###### main()

def main():

    helper.greetings()

    try:
        with open(argv[1]) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except:
        print("Usage: python3 main.py repo-structure.yml")
        exit(1)

    print("Loading the YML file...")
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

    # Download and generate focus-areas markdowns from bash script
    for key, values in data['focus-areas'].items():
        subprocess.check_call(['./get_focus_areas.sh', key, values])

    del data['focus-areas']

    for key, values in data.items():

        if values['include-wg-flag']:

            print("\nCloning '{}' from '{}' branch\n".format(key, values['github-branch']))
            subprocess.check_call(['git', 'clone', '-b', values['github-branch'], values['github-link'], key])

            # generate markdown for WG names
            paths = helper.generate_WG_md(values['wg-name'], 1, paths)

            paths = generate_paths(values, paths)

        else:
            print('[WARNING]: Flag off for {}, ignoring this WG'.format(key))

    helper.decrease_level(paths)
    generate_PDF(paths)

if __name__ == '__main__':
    main()