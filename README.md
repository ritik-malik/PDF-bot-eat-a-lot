# py-PDF-bot

A prototype pipeline that uses CHAOSS markdown files to auto-generate the corresponding LaTeX PDF using pandoc

This repository is mainly to test the idea of using YML file for the actual task using a very bare minimun setup

No error handling or extra stuff has been implemented so far

### Link to the [final output PDF](output/output.pdf)

## Requirements

* LaTeX : `sudo apt-get install texlive-full` [Debian-based]
* pyyaml : `pip3 install pyyaml`

## Working setup

1. Clone the repository
2. Change to src repository \
`cd src`
3. Confirm the configuation in `repo-structure.yml`
4. Run the main script \
`python3 main.py repo-structure.yml`
5. The final output PDF will be generated in the [`output`](output) directory

## Explanation

Refer to the [`README`](src) in src directory for explanation
