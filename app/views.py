# Shortener views
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages #import messages
# Model
from .models import Shortener
# Custom form
from .forms import ShortenerForm

# Create your views here.

def home_view(request):
    
    template = 'index.html'
    context = {}

    # Empty form
    context['form'] = ShortenerForm()

    if request.method == 'GET':
        return  render(request, template, context)

    elif request.method == 'POST':

        long = request.POST.get('long_url')
        url = Shortener.objects.filter(long_url=long)

        used_form = ShortenerForm(request.POST)

        if used_form.is_valid() and not url.exists():
            
            shortened_object = used_form.save()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url 
             
            context['new_url']  = new_url
            context['long_url'] = long_url
            messages.success(request, f"Your new url {new_url} is been created!" )
            return  render(request, template, context)

        elif url.exists():
            old_url = request.build_absolute_uri('/') + Shortener.objects.get(long_url=long).short_url
            long_url = Shortener.objects.get(long_url=long).long_url

            context['new_url'] = old_url
            context['long_url'] = long_url
            messages.info(request, f"Your url {long_url} already exists at {old_url} !" )

        context['errors'] = used_form.errors

        return render(request, template, context)


def redirect_url_view(request, shortened_part):

    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1        
        shortener.save()
        
        return HttpResponseRedirect(shortener.long_url)
        
    except:
        messages.warning(request, 'Sorry this link is broken :(' )
        raise Http404('Sorry this link is broken :(')