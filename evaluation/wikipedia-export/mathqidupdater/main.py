import pywikibot

site = pywikibot.Site()
page = pywikibot.Page(site, u"User:ZentralBot")
text = page.text
formula = 'E=mc^2'
qid = 35875
search = f'<math>{formula}</math>'
replace = f'<math qid=Q{qid}>{formula}</math>'
page.text = text.replace(search, replace, 1)
page.save(u"Add qID")
