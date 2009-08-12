
from south.db import db
from django.db import models
from pressroom.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Article.enable_comments'
        db.add_column('pressroom_article', 'enable_comments', models.BooleanField(default=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Article.enable_comments'
        db.delete_column('pressroom_article', 'enable_comments')
        
    
    
    models = {
        'pressroom.article': {
            'Meta': {'ordering': "['-pub_date']", 'get_latest_by': "'pub_date'"},
            'author': ('models.CharField', [], {'max_length': '100'}),
            'body': ('models.TextField', ['"Body text"'], {}),
            'documents': ('models.ManyToManyField', ["orm['pressroom.Document']"], {'related_name': "'articles'", 'null': 'True', 'blank': 'True'}),
            'enable_comments': ('models.BooleanField', [], {'default': 'True'}),
            'headline': ('models.CharField', [], {'max_length': '200'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'photos': ('models.ManyToManyField', ["orm['photologue.Photo']"], {'related_name': "'articles'", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('models.DateTimeField', ['"Publish date"'], {'default': 'datetime.datetime.now'}),
            'publish': ('models.BooleanField', ['"Publish on site"'], {'default': 'True'}),
            'sections': ('models.ManyToManyField', ["orm['pressroom.Section']"], {'related_name': "'articles'"}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {})
        },
        'photologue.photo': {
            'Meta': {'ordering': "['-date_added']", 'get_latest_by': "'date_added'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'pressroom.section': {
            'Meta': {'ordering': "['title']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {}),
            'title': ('models.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'pressroom.document': {
            'Meta': {'ordering': "['-pub_date']", 'get_latest_by': "'pub_date'"},
            'file': ('models.FileField', ['"Document"'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('models.DateTimeField', ['"Date published"'], {'default': 'datetime.datetime.now'}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {}),
            'title': ('models.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['pressroom']
