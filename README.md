# Introduction

Mathematical formulae are a significant part of scientific documents (books, articles, web pages, etc.) in the fields of science, technology, engineering, and mathematics (STEM). 
In most of the current information retrieval approaches, mathematical formulae are not considered, even though they are very common in texts within STEM fields.
Since mathematical formulae contain a lot of important information, they should not be ignored when analyzing and comparing documents.
Currently, there is no large labeled dataset available, containing mathematical formulae annotated with their semantics, that could be used to train machine learning models. 
\>>AnnoMathTeX<< offers a first approach to facilitate the annotation of mathematical formulae in STEM documents.
It recommends names for formulae and their constituting identifiers (characters/symbols, e.g. constants and variables) to the user who is annotating the 
document and thus enables the creation of a labeled dataset.


### Definitions

##### Identifiers
Identifiers in mathematical formulae are the meanings attached to symbols contained within a formula. For example, the identifier *E* means "*energy*" in the formula *E=mc^2*.

##### Formula Concept
The concept of a formula is the name or meaning (semantics) that can be associated with it. 
For example, a possible concept name annotation for the formula *E=mc2* would be "*mass-energy equivalence*".


# \>>AnnoMathTeX<<
AnnoMathTeX is a standalone web-based LaTeX text and formula annotation recommendation tool for STEM documents, implemented with the python framework django. 
It allows users to annotate identifiers contained in mathematical formulae, as well as entire formulae contained in a document with possible concept names selected from a list of suggested recommendations. 

<!---The recommendations are extracted from a number of different sources.

([Wikidata](https://www.wikidata.org) being one of them, in which case the selected token is annotated
with the [Wikidata QID](https://en.wikipedia.org/wiki/Wikidata#Items).)--->

<!---## Motivation--->


<!--- Maybe exclude this? --->
The recommendations for the formulae and identifer concept names are taken from four different sources:
* arXiv: A list containing names for all lower- and upper-case Lating and Greek letter identifiers appearing in the [arXiv corpus](http://ntcir-math.nii.ac.jp/data/) as text surrounding the identifiers, ranked by the frequency of their appearence.
* Wikipedia: A list containing identifier names for all letters appearing in Wikipedia articles as surrounding text, ranked by the frequency of their appearence.
* Wikidata: A SPARQL query to the [Wikidata Query Services API](https://query.wikidata.org) retrieves a list of matching [wikidata items](https://en.wikipedia.org/wiki/Wikidata#Items).
* Word Window: Nouns and proper nouns from the text of the annotated document surrounding the formula. The idea being, that the text surrounding the formula will often explain the formula and its parts. Consider this example from the Wikipedia article on the [Mass-energy equivalence](https://en.wikipedia.org/wiki/Mass–energy_equivalence):
   
  "*In physics, **mass–energy equivalence** states that anything having **mass** has an equivalent amount of **energy** and vice versa, with these fundamental quantities directly relating to one another by Albert Einstein's famous formula:*

  *E=mc^2*"
  
  The sentence directly preceding the formula, contains the word *"**mass**"*, which corresponds to the identifier *"m"* and the word *"**energy**"*, which corresponds to the identifier *"E"*. Furthermore, *"**mass–energy equivalence**"* describes the meaning of the entire formula.
 
<!---The vision for >>AnnoMathTeX<< is that it will enable the creation of a large and labeled dataset of identifiers and formulae with their corresponding concepts.
This dataset could be used to train models for all sorts of recommendation and recognition tasks involving mathematical symbols.--->

<!--## Features

What makes your project stand out? Include logo/demo screenshot etc.-->



<!---### Include:
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
* 10 recommendations per source (less if 10 not present)
* (recommended formats being .tex or .txt)--->

## Components/Modules/Workflow

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/overview.png"/>
</p>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python version >=3.6 is recommended. 


### Installing

Clone or download the repository. In your shell navigate to the folder [AnnoMathTeX](/AnnoMathTeX) and create & activate
a new virtual environment. Then run the command
```
pip install -r requirements.txt
```



<!--End with an example of getting some data out of the system or using it for a little demo-->

<!--## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.
-->

## Usage

### Start The Server

In a terminal navigate to the folder where the manage.py file is located ([AnnoMathTeX/annomathtex](/AnnoMathTeX/annomathtex))
and run the command
```python
python manage.py runserver
```

### Select a File

Open a browser window and navigate to [localhost:8000](http://127.0.0.1:8000). 

Select the file that you would like to annotate with the file browser.

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/upload.gif"/>
</p>


After selecting and uploading the file you will see the processed and rendered document in your browser window. You can now start annotating.
Mathematical environments are enclosed with highlighted dollar signs, and the identifiers are highlighted.
All other characters that are not to be annotated in the mathematical environment are coloured in grey.

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/uploaded_file.png"/>
</p>


### Annotating an Identifier

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/global_select.gif"/>
</p>

To annotate an identifier, simply click on the highlighted character (e.g. "E") in the document and you will see a pop-up with a table of recommendations.
To select one of the suggested recommendations, click on the matching cell, and it will be highlighted (along with all other matching cells from different sources).
The annotated identifier will be highlighted in green, and a table holding all the annotations that have been made is constructed at the top of the document.
If you unselect/cancel annotations. 
If none of the recommendations match, you can manually enter a name.

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/no_match.gif"/>
</p>

### Types of Annotations
Two different types of annotations are possible: A global annotation, and a local annotation. 

#### Global Annotation
By default the anotation mode is set to global annotation. This means that if you anntotate, e.g. the identifier *E* with "*energy*", all occurences of this identifier in the document will automatically receive this annotation.

#### Local annotation
To annotate an identifier locally (meaning that only this occurence of the identifier will be annotated), select the "*local*" option at the top of the table.

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/local.gif"/>
</p>


### Saving the annotations
To save the anntotations, simply click the "*save*" button at the top left of the page. This will write the annotations to a json file and create a csv file containing an evaluation table with comparison of the performance of the different sources.

<p align="center">
  <img src="https://github.com/philsMINT/AnnoMathTeX/blob/master/media/save.gif"/>
</p>

If you open the same file again at a later point in time, the annotations you made previously will be reloaded and you can continue right where you left off.


## Evaluation

### Results

For each file, an evaluation table of the following format is constructed.

| Identifier | Name               | arXiv | Wikipedia | Wikidata | WordWindow | Type   |
|:----------:|:------------------:|:-----:|:---------:|:--------:|:----------:|:------:|
| X          | variable           | -     | 6         | -        | 1          | global |
| p          | *manual insertion* | -     | -         | -        | -          | global |
| f          | function           | 2     | -         | -        | -          | local  |


The identifier *X* was annotated globally with "*variable*", which was found in the recommendations from the Wikipedia list and from the word window (positions 6 and 1 in the column respectively).
For the identifier *p* no matches were found; it was annotated with "*no match*".
The identifier "*f*" was annotated locally with "*function*", which was found in the recommendations from the arXiv list at position 2.


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details

<!--## Built With

* [Django](https://www.djangoproject.com) - The web framework used-->

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/AnnoMathTeX/contributing) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* Ian Mackerracher
* Philipp Scharpf

See also the list of [contributors](https://github.com/philsMINT/AnnoMathTeX/contributors) who participated in this project.

## Acknowledgments

We thank...
