import sys

import pywikibot
import logging
import mathqidupdater.annotation_reader as reader
from mathqidupdater.wikitext_replacer import WikitextReplacer
from mathqidupdater.build_sandboxes import get_final_pagelist, prefix

site = pywikibot.Site()


def process_page(name):
    page = pywikibot.Page(site, 'User:Physikerwelt/sandbox/' + name)
    replacements = reader.get_qids(f'{prefix}/{name}.csv')
    replacer = WikitextReplacer(page.text, replacements)
    oldid = page.latestRevision()
    new_text = replacer.replace_math_tags()
    if page.text == new_text:
        logging.info(f'skipping {name} nothing was changed')
        return
    page.text = new_text
    page.save(f'Add qids to {name} page')
    newid = page.latestRevision()
    logging.info(f'Review the changes at https://en.wikipedia.org/w/index.php?type=revision&diff={newid}&oldid={oldid}')


def add_qids():
    for name in get_final_pagelist():
        process_page(name[:-4])


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    add_qids()
