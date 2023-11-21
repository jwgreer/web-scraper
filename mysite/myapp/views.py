from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link
from django.http import HttpResponseRedirect

# Create your views here.

def scrape(request):

    if request.method == 'POST':
        site = request.post.get('site', '')
        try:
            page = requests.get(site)
            page.raise_for_status()  
        except requests.exceptions.RequestException as e:
            return render(request, 'myapp/error.html', {'error_message': str(e)})

        soup = BeautifulSoup(page.content, 'html.parser')

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)
        
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()

    return render(request, 'myapp/result.html', {'data': data})

def clear(request):
    Link.objects.all().delete()
    return render(request, 'myapp/result.html')