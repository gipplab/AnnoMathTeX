from django.shortcuts import render
from django.views.generic import TemplateView
from collections import OrderedDict
import json




class TestView(TemplateView):
    #template_name = "render_file_template.html"
    template_name = "test2.html"


def test_view(request):
    """d = {'sentences':[
                        ['word01', "word02"],
                        ['word11', "word12", "word13", "word14"],
                        ['word21', "word22", "word23", "word24," "word25"]
                     ]
        }"""


    d = OrderedDict({'sentences':
                         {'sentence0': ['word01', "word02"]
                          }
         })

    #d = {'s': 5}
    json_string = json.dumps(d)
    return render(request,
                  'test_template_d3.html',
                  {'TexFile': json_string})


