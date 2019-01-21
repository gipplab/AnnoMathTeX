"""
Math environment handling involves the revognition of formulae and identifiers.
These have to be recognised as being individual parts.
Then values from the surrounding text (NLP) should be associated with them,
and/or the corresponding wikidata Qid added.

Wikidata Qid can be extracted using
    - pywikibot
    - sparql

Steps:
    - extract math environment
    - extract identifiers
    - extract formulae
    - access wikidata
    - find Qid

Ideas:
    - Crawl wikidata, extracting all physical quanities

"""

import pywikibot

class WikidataQidPywikibot:
    """
    Useful properties:
        - P527: has part. E.g. mass-energy equivalence (E=mc^2, Q35875) has part energy (E, Q11379)
        - P361: part of. Inverse property of has part
        - P2534: defining formula. E.g. defining formula of mass-energy equivalence: E=mc^2
        - P1993: TeX string

    Claim object useful properties:
        - get_sources()
        -get_target()

    pywikibot.category - listify
    """
