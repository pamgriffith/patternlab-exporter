from django.shortcuts import render

from hero.models import Hero
from features.models import Feature
 
def index(request):
    hero = Hero.objects.all()
    features = Feature.objects.all()
    for feature in features:
    	feature.img_src = feature.img_src.url
    return render(request, 'templates/homepage.html', {'features': features, 'hero': hero})