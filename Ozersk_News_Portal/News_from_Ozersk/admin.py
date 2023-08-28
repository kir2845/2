from django.contrib import admin
from .models import Category, New, Author1, NewCategory


# создаём новый класс для представления товаров в админке
class NewAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('name', 'author', 'time_in') # оставляем только имя и цену товара
    list_filter = ('name', 'author', 'time_in')  # добавляем примитивные фильтры в нашу админку
#    search_fields = ('name', 'author', 'time_in')  # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Category)
#admin.site.register(New)
admin.site.register(Author1)
admin.site.register(NewCategory)
admin.site.register(New, NewAdmin)




