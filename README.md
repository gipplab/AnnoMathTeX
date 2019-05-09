# \>>AnnoMathTeX<<

AnnoMathTeX is a LaTeX text and formula annotation recommendation tool for STEM (Science, Technology, Engineering, 
Mathematics) documents. It allows users to annotate 
identifiers in mathematical formulae, the entire formula as well as the named entities contained in a document 
(recommended formats being .tex or .txt) with the corresponding concept. Theses concepts are extracted from a number of 
different sources.

[Wikidata](https://www.wikidata.org) being one of them, in which case the selected token is annotated
with the [Wikidata QID](https://en.wikipedia.org/wiki/Wikidata#Items).

## Motivation
Machine Learning has proven time and time again to be extremely useful in classification tasks. However, very large 
amounts of labeled data are necessary to train machine learning methods. Currently, there is no large enough labeled 
dataset containing mathematical formulae annotated with their semantics available, that could be used to train machine 
learning models. >>AnnoMathTeX<< offers a first approach to facilitate the annotation of mathematical formulae in STEM 
documents, by recommending the concept associated to a certain identifier of formula to the user who is annotating the 
document.

The recommendations for the concepts are taken from four different sources:
* arXiv: A list containing identifiers appearing in the arXiv corpus with the corresponding concepts, ranked by frequency of appearence.
* Wikipedia: A list containing identifiers appearing in Wikipedia articles with the corresponding concepts, ranked by frequency of appearence.
* Wikidata: A Sparql query to the [Wikidata Query Services API](https://query.wikidata.org) retrieves a list of matching [wikidata items](https://en.wikipedia.org/wiki/Wikidata#Items).
* Word Window: Nouns and proper nouns from the text surrounding the formula. The idea being, that the text surrounding the formula will often explain the formula its parts. Consider this example from the Wikipedia article on the [Mass-energy equivalence](https://en.wikipedia.org/wiki/Mass–energy_equivalence):
   
  *"In physics, **mass–energy equivalence** states that anything having **mass** has an equivalent amount of **energy** and vice versa, with these fundamental quantities directly relating to one another by Albert Einstein's famous formula:*

  *E=mc^2"*
  
  The sentence directly preceding the formula, contains the word *"**mass**"*, which corresponds to the identifier *"m"* and the word *"**energy**"*, which corresponds to the identifier *"E"*. Furthermore, *"**mass–energy equivalence**"* describes the meaning of the entire formula.
 
The vision for >>AnnoMathTeX<< is that it will enable the creation of a large and labeled dataset of identifiers and formulae with their corresponding concepts.
This dataset could be used to train models for all sorts of recommendation and recognition tasks involving mathematical symbols.
## Features

What makes your project stand out? Include logo/demo screenshot etc.





### Include:
* annotations saved and possible to reload later
  * enables saving and reloading
  * multiple people working on same file at same time
* different sources with functionality easy to add others
* global annotations
* local annoations
* reject all recommendations
* highlighting in text to show feedback to user about already handled tokens
* highlighting in table to show to user which concept was chosen
* annotations shown in table at top of document that updates in real time with the current annotations
* Evaluation file
  * per annotation
  * which sources contained the conecpt that the user selected for the annotation
  * which position the selected concept had in the column.
* Randomized and anonymzed recommendation sources, or information shown to user.

## Components/Modules/Workflow

Visualize an overview of the different components/modules of the system as well as the workflow and describe the individual parts

## Very Short Code Examples

Show what the library does as **concisely** as possible, developers should be able to figure out **how** your project solves their problem by looking at the code example. Make sure the API you are showing off is obvious, and that your code is short and concise. See the [news-please project](https://github.com/fhamborg/news-please/blob/master/README.md#use-within-your-own-code-as-a-library) for example.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

Python version >=3.6 is recommended.
Django 


```
Give examples
```

### Installing

Clone or download the repository. In your shell navigate to the folder [AnnoMathTeX](/AnnoMathTeX) and create & activate
a new virtual environment. Then run the command
```
pip install -r requirements.txt
```



End with an example of getting some data out of the system or using it for a little demo

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Usage

### Start The Server

In a terminal navigate to the folder where the manage.py file sits ([AnnoMathTeX/annomathtex](/AnnoMathTeX/annomathtex))
and run the command
```python
python manage.py runserver
```

### Select a File

Open a browser window and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000). 

Select the file that you would like to annotate with the file browser.

![](https://github.com/philsMINT/AnnoMathTeX/blob/master/media/upload.gif)

After selecting and uploading the file you will see the processed and rendered document in your browser window. You can now start annotating.
Nouns, proper nouns and named entities are highlighted in the natural language part of the document. They are also shown as recommendations for annotation in the word window.
Mathematical environments are enclosed with highlighted dollar signs, and the identifiers are highlighted with yet another colour.
All other symbols in the mathematical environment are coloured in grey, as they are not interesting for the purpose of annotation.

![](https://github.com/philsMINT/AnnoMathTeX/blob/master/media/uploaded_file.png)


### Annotating an Identifier

![](https://github.com/philsMINT/AnnoMathTeX/blob/master/media/global_select.gif)

To annotate an identifier, simply click on the highlighted character (e.g. "E") in the document and you will be presented with a table of recommendations.
To select one of the suggested recommendations, select the matching cell, and it will be highlighted (along with all other mathcing cells from different sources).
The annotated identifier will be highlighted in a different colour, and a table holding all the annotations is constructed at the top of the document.
If you click a highlighted cell, your annotation will be reversed. 

### Types of Annotations
Two different types of annotations are possible: A global annotation, and a local annotation. 




## Results

If you are about to complete your project, include your preliminary results that you also show in your final project presentation, e.g., precision/recall/F1 measure and/or figures highlighting what your project does with input data. If applicable, at first briefly describe the dataset your created/use and the use cases.

If you are about to complete your thesis, just include the most important findings (precision/recall/F1 measure) and refer the to the corresponding pages in your thesis document.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details

## Built With

* [Django](https://www.djangoproject.com) - The web framework used

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/AnnoMathTeX/contributing) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* Ian Mackerracher
* Philipp Scharpf
See also the list of [contributors](https://github.com/philsMINT/AnnoMathTeX/contributors) who participated in this project.

## Acknowledgments

We thank...
