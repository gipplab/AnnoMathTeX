import pywikibot

site = pywikibot.Site()
page = pywikibot.Page(site, 'Harmonic_oscillator')
text = page.text
fh =  open('../tests/data/Harmonic_oscillator.txt', 'w',encoding='utf-8')
fh.write(text)
fh.close()
# formula = 'E=mc^2'
# qid = 35875
# search = f'<math>{formula}</math>'
# replace = f'<math qid=Q{qid}>{formula}</math>'
# page.text = text.replace(search, replace, 1)
# page.save(u"Add qID")
