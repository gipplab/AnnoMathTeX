import pywikibot
import mathqidupdater.annotation_reader as reader

def build_sandbox(name):
    site = pywikibot.Site()
    page = pywikibot.Page(site, name)
    text = page.text
    sandbox = pywikibot.Page(site, 'User:Physikerwelt/sandbox/'+name)
    sandbox.text = text
    sandbox.save(f'Create sandbox copy of {name} page')

def get_final_pagelist():
    # Refers to git@github.com:ag-gipp/dataAnnoMathTex.git commit b477ce9c139ca4f7cfca71b9dc9643e1e47b38cc
    prefix  = '../../../dataAnnoMathTex/evaluation/'
    return reader.get_file_list(prefix)

def build_sandboxes():
    for name in get_final_pagelist():
        build_sandbox(name[:-4])

build_sandboxes()

