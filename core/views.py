from django.shortcuts import render
from Stores.models import Store

def home(request):
    stores = Store.objects.filter(active=True)
    for store in stores:
        store.latitude = str(store.latitude).replace(",", ".")
        store.longitude = str(store.longitude).replace(",", ".")
    return render(request, 'stores/index.html', {'stores': stores})