from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import User, Profile, AccessToken, Stock, StockPriceCurrent, Favourites, Transaction

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(AccessToken)
admin.site.register(Stock)
admin.site.register(StockPriceCurrent)
admin.site.register(Favourites)
admin.site.register(Transaction)