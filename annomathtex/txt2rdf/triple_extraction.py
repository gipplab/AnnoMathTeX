import nltk

from pycorenlp import StanfordCoreNLP

#text = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'
text = "Novartis International AG is a Swiss multinational pharmaceutical company based in Basel, Switzerland. It is one of the largest pharmaceutical companies by both market capitalization and sales. Novartis manufactures the drugs clozapine (Clozaril), diclofenac (Voltaren), carbamazepine (Tegretol), valsartan (Diovan), imatinib mesylate (Gleevec/Glivec), ciclosporin (Neoral/Sandimmun), letrozole (Femara), methylphenidate (Ritalin), terbinafine (Lamisil), and others. In 1996, Ciba-Geigy merged with Sandoz; the pharmaceutical and agrochemical divisions of both companies formed Novartis as an independent entity. Other Ciba-Geigy and Sandoz businesses were sold, or, like Ciba Specialty Chemicals, spun off as independent companies. The Sandoz brand disappeared for three years, but was revived in 2003 when Novartis consolidated its generic drugs businesses into a single subsidiary and named it Sandoz. Novartis divested its agrochemical and genetically modified crops business in 2000 with the spinout of Syngenta in partnership with AstraZeneca, which also divested its agrochemical business."
#text = "The Sun is the star at the center of the Solar System. It is a nearly perfect sphere of hot plasma,[15][16] with internal convective motion that generates a magnetic field via a dynamo process.[17] It is by far the most important source of energy for life on Earth. Its diameter is about 1.39 million kilometers (864,000 miles), or 109 times that of Earth, and its mass is about 330,000 times that of Earth. It accounts for about 99.86% of the total mass of the Solar System.[18] Roughly three quarters of the Sun's mass consists of hydrogen (~73%); the rest is mostly helium (~25%), with much smaller quantities of heavier elements, including oxygen, carbon, neon, and iron.[19]"
#text = "It is a nearly perfect sphere of hot plasma,[15][16] with internal convective motion that generates a magnetic field via a dynamo process."
#text = "Soker and Dgani (1997) conduct a theoretical study of the processes involved when the ISM magnetic field is important in the interaction. In the case where the ISM is fully ionized, we define four characterizing velocities of the interaction process: the adiabatic sound speed and the Alfven velocity of the ISM, the expansion velocity of the nebula, and the relative velocity of the PN central star and the ISM. Both the thermal and magnetic pressure increase substantially behind a strong shock. If radiative cooling is rapid, however, the magnetic pressure will eventually substantially exceed the thermal pressure, leading to several strong MHD instabilities around the nebula, and probably to magnetic field reconnection behind the nebula and negligible cooling behind the shock. The thermal pressure, which grows more than the magnetic pressure in a strong shock, will dominate behind the shock.  Magnetic field reconnection is not likely to occur behind the nebula. This domain characterizes the interaction of the solar wind with the atmospheres of Venus and Mars."
#text = "String theory is a broad and varied subject that attempts to address a number of deep questions of fundamental physics. String theory has been applied to a variety of problems in black hole physics, early universe cosmology, nuclear physics, and condensed matter physics, and it has stimulated a number of major developments in pure mathematics. Because string theory potentially provides a unified description of gravity and particle physics, it is a candidate for a theory of everything, a self-contained mathematical model that describes all fundamental forces and forms of matter. Despite much work on these problems, it is not known to what extent string theory describes the real world or how much freedom the theory allows in the choice of its details."
#text = "The Germany national football team (German: deutsche Fußballnationalmannschaft or Die Mannschaft) is the men's football team that has represented Germany in international competition since 1908.[6] It is governed by the German Football Association (Deutscher Fußball-Bund), founded in 1900.[10][11] Ever since the DFB was reinaugurated in 1949 the team has represented the Federal Republic of Germany. Under Allied occupation and division, two other separate national teams were also recognised by FIFA: the Saarland team representing the Saarland (1950–1956) and the East German team representing the German Democratic Republic (1952–1990). Both have been absorbed along with their records[12][13] by the current national team. The official name and code Germany FR (FRG) was shortened to Germany (GER) following the reunification in 1990."
#text = "SAP SE Systeme, Anwendungen und Produkte in der Datenverarbeitung, Systems, Applications & Products in Data Processing, is a German-based European multinational software corporation that makes enterprise software to manage business operations and customer relations. SAP is headquartered in Walldorf, Baden-Württemberg, Germany with regional offices in 180 countries. The company has over 335.000 customers in over 180 countries. The company is a component of the Euro Stoxx 50 stock market index."

#text = "the quick brown fox jumps over the lazy dog."

#################
# NLTK POS-tagger
#################

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def extract_triples_nltk():

    # nltk.help.upenn_tagset()
    tagged = preprocess(text)
    noun_verb_list = []
    for entity in tagged:
        if entity[1].startswith("V") or entity[1].startswith("N"):
            noun_verb_list.append(entity)

    for idx in range(0,len(noun_verb_list)):
        if noun_verb_list[idx][1].startswith("V"):

            # verb
            V = noun_verb_list[idx][0]

            subjects = []
            objects = []

            for i in range(1,idx+1):
                # look for subject before verb
                candidate = noun_verb_list[idx-i]
                if candidate[1].startswith("N"):
                    subjects.append(candidate[0])

            for i in range(1,len(noun_verb_list)-idx):
                # look for object after verb
                candidate = noun_verb_list[idx+i]
                if candidate[1].startswith("N"):
                    objects.append(candidate[0])

            # take closest candidate
            try:


                subject_list = []
                object_list = []
                for i in range(0,1):
                    try:
                        subject_list.append(subjects[i])
                    except:
                        pass
                    try:
                        object_list.append(objects[i])
                    except:
                        pass
                S = subject_list
                O = object_list

                # S = subjects
                # O = objects

                print("{" + str(S) + "," + V + "," + str(O) + "}")

            except:
                pass

# RUN NLTK extraction
extract_triples_nltk()

#########################
# Stanford CoreNLP OpenIE
#########################

# paper: https://nlp.stanford.edu/pubs/2015angeli-openie.pdf

def extract_triples_openie():

    # run corenlp server from shell
    # java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "openie" -port 9000 -timeout 30000
    # http://corenlp.run/
    nlp = StanfordCoreNLP("http://localhost:9000")
    output = nlp.annotate(text, properties={
        #'annotators': 'tokenize, ssplit, pos, depparse, parse, openie',
        'annotators': 'openie',
        'outputFormat': 'json'
        })

    #print(output['sentences'][0].keys)

    for sentence in output['sentences']:

        for result in sentence['openie']:
            print("{" + result['subject'] + ", " + result['relation'] + ", " + result['object'] + "}")

# RUN OpenIE extraction
#extract_triples_openie()