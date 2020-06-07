#from hawk import settings
from . import settings

def theme(request):
    return {'THEME': settings.THEME}