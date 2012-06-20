from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q
from photologue.models import Photo
from models import Document

class PhotoLookup(LookupChannel):

    model = Photo

    def get_query(self,q,request):
        return Photo.objects.filter(Q(caption__icontains=q) | Q(title__istartswith=q)).order_by('title')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.title

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div>%s<br><i>%s</i></div>" % (escape(obj.title),obj.admin_thumbnail(),escape(obj.caption))

class DocumentLookup(LookupChannel):

    model = Document

    def get_query(self,q,request):
        return Document.objects.filter(Q(summary__icontains=q) | Q(title__istartswith=q) | Q(file__istartswith=q)).order_by('title')

    def get_result(self,obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.title

    def format_match(self,obj):
        """ (HTML) formatted item for display in the dropdown """
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><b>%s</b></div><div><i>%s</i></div>" % (escape(obj.file), escape(obj.title),escape(obj.summary))