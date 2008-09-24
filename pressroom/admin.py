from django.contrib import admin
from models import Article, Document, Section

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('headline',)}
    list_display = ('headline', 'author', 'pub_date', 'publish')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    save_as = True
    
class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']

class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Section, SectionAdmin)
    
