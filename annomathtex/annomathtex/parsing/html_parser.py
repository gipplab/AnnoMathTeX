###################################################################################
###################################################################################
###################################################################################
#################################### NOT USED #####################################
###################################################################################
###################################################################################
###################################################################################



#todo: implement





from bs4 import BeautifulSoup
import re
import warnings
warnings.filterwarnings("ignore")


def foo(request_file):
    soup = BeautifulSoup(request_file)
    #print(soup.prettify())
    #print(request_file.read())

    ignore = [r'\n', '', r'\s']
    #for a in list(soup.find_all('math')):
        #print(a.contents)
    #    b = ' '.join(i for i in a.contents if i not in ignore)
    #    print(type(b))
    #print(soup.get_text())
    math_envs = list(
        map(
            lambda math_env: ' '.join(chunk for chunk in math_env.contents if chunk not in ignore),
            list(soup.find_all('math'))
        )
    )
    print(math_envs)



def preprocess(request_file):
    file_replace_math_opening = request_file.replace('<math>', '$')
    file_replace_math_closing = file_replace_math_opening.replace('</math>', '$')
    return file_replace_math_closing


s = """
provides a more sophisticated though more computationally expensive way to perform ''k''-means. It is still a heuristic method.

<math>\phi(S_j) </math>is the individual cost of <math>S_j</math> defined by <math>\sum_{x \in S_j} (x - \mu_j)^2</math>, with <math>\mu_j</math> the center of the cluster.
"""
