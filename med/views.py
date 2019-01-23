from django.shortcuts import render
from django.template.context_processors import csrf


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)


def index(request):
    return form({}, 'med/index.html', request)
