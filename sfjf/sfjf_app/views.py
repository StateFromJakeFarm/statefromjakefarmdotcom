from django.shortcuts import render

def home(request):
    '''
    Render homepage
    '''
    return render(request, 'base.html')
