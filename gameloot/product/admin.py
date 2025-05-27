from django.contrib import admin
from .models import sign, Produit, Commande, category

@admin.register(sign)
class SignAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('user', 'produit', 'quantite', 'date_commande')
    list_filter = ('date_commande',)

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')