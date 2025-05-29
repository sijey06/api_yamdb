from django.contrib import admin
from .models import Title, Category, Genre, GenreTitle

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)


