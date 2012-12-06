from django.contrib import admin
from django.conf import settings
from models import Article, Document, Section
from imperavi.admin import ImperaviAdmin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class ArticleAdminBase(admin.ModelAdmin):
    list_display = ('headline', 'author', 'language', 'pub_date', 'publish', 'modified_by')
    search_fields = ('headline', 'author', 'summary', 'body')
    list_filter = ['pub_date', 'author', 'language']
    date_hierarchy = 'pub_date'
    save_on_top = True
    filter_horizontal=('sections',)

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        obj.save()

    def formfield_for_dbfield(self, field, **kwargs):
        if field.name == 'author':
            author = u''
            if 'request' in kwargs:
                request = kwargs['request']
                if request.user:
                    if request.user.get_full_name():
                        author = request.user.get_full_name()
                    elif request.user.username:
                        author = request.user.username
            kwargs['initial'] = author
        return super(ArticleAdminBase, self).formfield_for_dbfield(field, **kwargs)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title',)

if 'imperavi' in settings.INSTALLED_APPS and 'ajax_select' in settings.INSTALLED_APPS:
    class ArticleAdmin(ArticleAdminBase, ImperaviAdmin, AjaxSelectAdmin):
        form = make_ajax_form(
            model=Article,
            fieldlist={
                'photos':'photos',
                'documents': 'documents',
                'translation_of': 'articles'
            }
        )
else:
    class ArticleAdmin(ArticleAdminBase):
        pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Section, SectionAdmin)
    
