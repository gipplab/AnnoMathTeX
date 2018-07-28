from flask import Flask, render_template, request, flash
from wtforms import Form, TextField, TextAreaField, StringField, SubmitField, validators
import easygui

#from identifier_retrieval import retrieve_identifier_semantics

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class AnnotationForm(Form):
    name = TextField('Name:', validators=[validators.required()])

class ContentForm(Form):
    content = StringField('content')

@app.route("/", methods=['GET', 'POST'])
def init():

    form = AnnotationForm(request.form)

    path = ""
    if request.method == 'POST':
        path = easygui.fileopenbox()

    return render_template('annotation_tool.html', tex=path)

if __name__ == '__main__':
    app.run(debug=True)