from django.db.models import F
from django.shortcuts import render

# Create your views here.
from apps.photos.models import Photo, PhotoCategory
from apps.statistic.views import add_visit


@add_visit
def album(request):
    categories = list(PhotoCategory.objects.filter(permission=1).values("id", "category", "cover__pic").
                      annotate(cover_pic=F("cover__pic")))
    context = {
        "categories": categories
    }
    return render(request, "photos.html", context=context)


@add_visit
def detail(request):
    category = request.path.split('/')[-1]
    photos = Photo.objects.filter(category__category=category).values("photo").annotate(url=F("photo"))

    for photo in photos:
        photo["name"] = photo["url"].split("/")[-1]
        photo["original_url"] = photo["url"].replace('/thumbnail/', '/preview/')

    context = {
        "category": category,
        "photos": photos,
    }
    return render(request, "photos.html", context=context)