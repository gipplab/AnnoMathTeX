import re
import logging
import shlex

import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode


# Adapted from https://phabricator.wikimedia.org/diffusion/TTEX/browse/master/mathwikibot.py

class WikitextReplacer:
    mathregex = re.compile(r'<math(.*?)>(.*?)</math\s*?>', flags=re.DOTALL | re.IGNORECASE)

    nowikipatterns = re.compile(
        r'(\<nowiki.*?\>.*?\<\/nowiki\>)|(\<pre.*?\>.*?\<\/pre\>)|(\<source.*?\>.*?\<\/source\>)|(\<syntaxhighlight.*?\>.*?\<\/syntaxhighlight\>)|(\<!--.*?--\>)',
        flags=re.DOTALL | re.IGNORECASE)
    wt: Wikicode
    text: str
    replacements: dict
    changed = False

    def allow_bots(self, user):
        user = user.lower().strip()
        text = mwparserfromhell.parse(self.text)
        for tl in text.filter_templates():
            if tl.name.matches(['bots', 'nobots']):
                break
        else:
            return True
        for param in tl.params:
            bots = [x.lower().strip() for x in param.value.split(",")]
            if param.name == 'allow':
                if ''.join(bots) == 'none': return False
                for bot in bots:
                    if bot in (user, 'all'):
                        return True
            elif param.name == 'deny':
                if ''.join(bots) == 'none': return True
                for bot in bots:
                    if bot in (user, 'all'):
                        return False
        if (tl.name.matches('nobots') and len(tl.params) == 0):
            return False
        return True

    def __init__(self, wikitext, repl):
        self.text = wikitext
        self.replacements = repl

    def replace_math_tags(self):
        nowikiloc = []
        done = []
        for nowiki in re.finditer(self.nowikipatterns, self.text):
            nowikiloc.append([nowiki.start(), nowiki.end()])
        for math in sorted(re.finditer(self.mathregex, self.text), reverse=True, key=lambda
                x: x.start()):  # get all math tags in reverse order such that the math.start() and math.end() positions can be used
            if self.is_nowikiloc(math, nowikiloc):
                continue
            tag_content = math.group(2)
            attribs = math.group(1)
            if tag_content in self.replacements:
                qid = self.replacements.get(tag_content)
                logging.info(f'Found target for Q{qid}.')
                if attribs.lower().__contains__('qid'):
                    logging.warning(f'Skipping Q{qid} as already contains qid in attributes: "{attribs}"')
                    # https://stackoverflow.com/a/23228582
                    attrib_dict = dict(x.split('=') for x in shlex.split(attribs))
                    if 'qid' in attrib_dict:
                        done_qid = attrib_dict['qid']
                        done_qid_int = re.sub(r'[^\d]', '', done_qid)
                        done.append(done_qid_int)
                        logging.warning(f'Skipping Q{done_qid_int} as already contained in article.')
                    continue
                if qid in done:
                    logging.warning(f'Skipping Q{qid} as already replaced above.')
                    continue
                done.append(qid)
                attribs += f' qid=Q{qid}'
                new_tag = f'<math{attribs}>{tag_content}</math>'
                logging.debug(f'Replacing "{math.group()}" with "{new_tag}"')
                self.text = self.text[:math.start()] + new_tag + self.text[math.end():]
                self.changed = True
        return self.text

    @staticmethod
    def is_nowikiloc(math, nowikiloc):
        for nw in nowikiloc:
            if nw[0] < math.start() and math.end() < nw[1]:
                return True  # complete math formula is inside nowiki
            elif nw[0] < math.start() < nw[1] or nw[0] < math.end() < nw[1]:
                return True  # one of the math tags is inside nowiki
        return False
