# Explanation

The following is the explanation of various scripts used :

* `main.py` : The main script to be run, takes a yml file as the only command line argument. This script inturn calls other scripts
* `helper.py` : To be imported by main script. Contains helper functions
* `repo-structure.yml` : The dynamic yml conf file that defines the structure and order of WG-common, WG-value, and their respective focus-areas READMEs from the CHAOSS/website repo
* `logs.txt` : A layout of output expected from the `main.py` script
* `side-scripts/get_focus_areas.sh` : A bash script to download focus-areas READMEs, split them individually, and create respective markdown file with specific naming convention
* `side-scripts/template.tex` : LaTeX template used by pandoc while generating the PDF
* `side-scripts/cover.tex` : A replication of CHAOSS coverpage in LaTeX
* `side-scripts/pygments.theme` : Theme used in PDF

Note: *Processing is performed in `test-env` directory, so all the files in that directory are temporary and are erased automatically before every use*

## Walkthrough

* Load the yml conf file
* Load the side scripts
* Cleanup test-env directory
* Call `get_focus_areas.sh`
    * Get focus-areas READMEs from CHAOSS/website
    * Split them into individual focus-areas
    * Rename files according to specific naming convention
* Clone the WG repositories
* Generate WG markdowns files for headings (using lorem-ipsum for now)
* Generate paths to metric markdown files in various WGs
* Decrease heading levels (only in metric markdowns) by 2 ##
* Call pandoc to generate the final PDF
* Move the final PDF to the output directory
