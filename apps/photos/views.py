from django.db.models import F
from django.shortcuts import render

# Create your views here.
from apps.photos.models import Photo, PhotoCategory
from apps.statistic.views import add_visit


@add_visit
def album(request):
    categorys = list(PhotoCategory.objects.values("id", "category", "cover__pic").annotate(cover_pic=F("cover__pic")))
    context = {
        "categorys": categorys,
    }
    return render(request, "photos.html", context=context)


@add_visit
def detail(request):
    category = request.path.split('/')[-1]
    photos = Photo.objects.filter(category__category=category).values("photo").annotate(url=F("photo"))

    for photo in photos:
        photo["name"] = photo["url"].split("/")[-1]
        if photo["name"].startswith("thumb-"):
            photo["name"] = photo["name"][6:]

    context = {
        "category": category,
        "photos": photos,
    }
    return render(request, "photos.html", context=context)