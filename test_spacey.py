import en_core_web_sm
import os

class SpaceyIdentifier:
    nlp = en_core_web_sm.load()
    test_text = "The case could escalate tensions between China and the US says Donald Trump."



    def tex_reader(self):
        with open(os.getcwd() + '/latexfiles/dgani_small.tex', 'r') as f:
            file = f.read()#.splitlines()

        return file

    def test(self):
        doc = self.nlp(self.tex_reader())
        #print(doc)
        #print([(X, X.ent_iob_, X.ent_type_) for X in doc])
        #print(self.nlp(str(doc)))
        #x = dict([(str(x), x.label_) for x in self.nlp(str(doc)).ents])
        x = dict([(str(x), x.label_) for x in self.nlp(self.test_text).ents])
        print(x)


    def test2(self):
        doc = self.nlp(self.tex_reader())
        sentences = [x for x in doc.sents]
        p = [(x.orth_, x.pos_, x.lemma_) for x in [y
                                               for y
                                               in self.nlp(str(sentences))
                                               if not y.is_stop and y.pos_ != 'PUNCT']]

        for v in p:
            print(v)


    def test3(self):
        doc = self.nlp(self.test_text)
        print([t for t in doc])


SpaceyIdentifier().test3()