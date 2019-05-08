###################################################################################
###################################################################################
###################################################################################
#################################### NOT USED #####################################
###################################################################################
###################################################################################
###################################################################################

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")


def foo(request_file):
    soup = BeautifulSoup(request_file)
    ignore = [r'\n', '', r'\s']
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
