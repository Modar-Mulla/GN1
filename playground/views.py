import json
from django.shortcuts import render
from . import utils
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'index.html')


@csrf_exempt
def calc(request):
    if request.method == "POST":
        body = json.loads(request.body)
        pop_size = int(body['population size'])
        max_itr = int(body['max iterations'])
        top = int(body['top'])
        best = utils.Main(pop_size, max_itr, top)
        best = json.dumps(best)
        return HttpResponse(best)
