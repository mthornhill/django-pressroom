from django.contrib import admin
from models import Article, Document, Section
from imperavi.admin import ImperaviAdmin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class ArticleAdmin(ImperaviAdmin, AjaxSelectAdmin):
    list_display = ('headline', 'author', 'pub_date', 'publish')
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    save_as = True
    filter_horizontal=('sections',)

    form = make_ajax_form(Article,{'photos':'photos', 'documents': 'documents'})

    
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Section, SectionAdmin)
    
