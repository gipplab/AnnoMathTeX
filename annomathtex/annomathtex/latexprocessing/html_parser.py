from bs4 import BeautifulSoup
import re


def foo(request_file):
    print('FOOOOOOO')
    soup = BeautifulSoup(request_file.read())
    #print(soup.prettify())
    #print(request_file.read())

    for a in list(soup.find_all('math')):
        print(a)
    #print(soup.get_text())



def preprocess(request_file):
    file_replace_math_opening = request_file.replace('<math>', '$')
    file_replace_math_closing = file_replace_math_opening.replace('</math>', '$')
    return file_replace_math_closing
