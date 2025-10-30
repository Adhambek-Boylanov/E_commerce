from django.contrib import admin
from configapp.models import User,Product,Review,FlashSale,Category
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(FlashSale)
admin.site.register(Category)