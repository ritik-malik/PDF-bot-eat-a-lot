# PDF-bot-eat-a-lot

A py bot that eats a lot of markdown files to auto-generate the corresponding LaTeX PDF using pandoc

This repository is mainly to test the idea of using YML file for the actual task using a very bare minimun setup

No error handling or extra stuff has been implemented so far

#### Link to the [final output PDF](output.pdf)

## Requirements

LaTeX : `sudo apt-get install texlive-full` [Debian-based]
pyyaml : `pip3 install pyyaml`

## Working

* Configure the WG repository structure in [`repo-structure.yml`](repo-structure.yml)
* This yml file already contains working templates for [wg-common](https://github.com/chaoss/wg-common) and [wg-value](https://github.com/chaoss/wg-value)

## Usage

* `python3 PDF-bot.py repo-structure.py`




