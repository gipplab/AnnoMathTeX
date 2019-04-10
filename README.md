#  How to use this file

We ask that all students working on their Bachelor or Master projects/theses have to hand in the source code and project documentation. Source code (including architecture and comments) has to adhere to our [developer guidelines](https://isgroup.atlassian.net/wiki/spaces/STUD/pages/1409184/Developer+Guidelines). The project documentation has to consist of a `README.md` file (optionally also more `.md` files if useful) that contains the following information. Thus, copy this file's content as a template in your project and revise it with your project's information.

Besides using the following template, also check out the following sources to see some examples or read further useful information on how to write a good `README.md` for your project. Note that the exemplary projects do not 100% follow this template (either because they are created by third-parties or were created before we consolidated all the information into this template) but are still examples of good `README.md` files.
* [Example: news-please](https://github.com/fhamborg/news-please/blob/master/README.md)
* [Article: How to write a good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
* [Article: A beginners guide to writing a good readme](https://medium.com/@meakaakka/a-beginners-guide-to-writing-a-kickass-readme-7ac01da88ab3)

Useful tools:
* [Recordit: record your screen and safe it to a GIF](http://recordit.co/)

# AnnoMathTeX

AnnoMathTeX is a LaTeX text and formula annotation recommendation tool for STEM documents. It allows users to annotate 
identifiers in mathematical formulae, the entire formula as well as the named entities contained in a document 
(recommended formats being .tex or .txt) with the corresponding concept. Theses concepts are taken from a number of 
different sources, [Wikidata](https://www.wikidata.org) being one of them, in which case the selected token is annotated
with the [Wikidata QID](https://en.wikipedia.org/wiki/Wikidata#Items).

## Motivation
Machine Learning has proven time and time again to be extremely useful in classification tasks. However, very large 
amounts of labeled data are necessary to train machine learning methods. Currently, there is no large enough labeled 
dataset containing mathematical formulae annotated with their semantics available, that could be used to train machine 
learning models.
## Features

What makes your project stand out? Include logo/demo screenshot etc.

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

## How to use? (maybe optional)

In a terminal navigate to the folder where the manage.py file sits ([AnnoMathTeX/annomathtex](/AnnoMathTeX/annomathtex))
and run the command
```python
python manage.py runserver
```
In your browser navigate to [http://127.0.0.1:8000/file_upload/](http://127.0.0.1:8000/file_upload/). Any browser should 
work, although we recommend using Google Chrome.

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
