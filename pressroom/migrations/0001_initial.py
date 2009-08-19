
from south.db import db
from django.db import models
from pressroom.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Article'
        db.create_table('pressroom_article', (
            ('id', models.AutoField(primary_key=True)),
            ('pub_date', models.DateTimeField("Publish date", default=datetime.datetime.now)),
            ('headline', models.CharField(max_length=200)),
            ('slug', models.SlugField()),
            ('summary', models.TextField(blank=True)),
            ('body', models.TextField("Body text")),
            ('author', models.CharField(max_length=100)),
            ('publish', models.BooleanField("Publish on site", default=True)),
        ))
        db.send_create_signal('pressroom', ['Article'])
        
        # Adding model 'Section'
        db.create_table('pressroom_section', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(unique=True, max_length=80)),
            ('slug', models.SlugField()),
        ))
        db.send_create_signal('pressroom', ['Section'])
        
        # Adding model 'Document'
        db.create_table('pressroom_document', (
            ('id', models.AutoField(primary_key=True)),
            ('file', models.FileField("Document")),
            ('pub_date', models.DateTimeField("Date published", default=datetime.datetime.now)),
            ('title', models.CharField(max_length=200)),
            ('slug', models.SlugField()),
            ('summary', models.TextField()),
        ))
        db.send_create_signal('pressroom', ['Document'])
        
        # Adding ManyToManyField 'Article.documents'
        db.create_table('pressroom_article_documents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm.Article, null=False)),
            ('document', models.ForeignKey(orm.Document, null=False))
        ))
        
        # Adding ManyToManyField 'Article.photos'
        db.create_table('pressroom_article_photos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm.Article, null=False)),
            ('photo', models.ForeignKey(orm['photologue.Photo'], null=False))
        ))
        
        # Adding ManyToManyField 'Article.sections'
        db.create_table('pressroom_article_sections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm.Article, null=False)),
            ('section', models.ForeignKey(orm.Section, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Article'
        db.delete_table('pressroom_article')
        
        # Deleting model 'Section'
        db.delete_table('pressroom_section')
        
        # Deleting model 'Document'
        db.delete_table('pressroom_document')
        
        # Dropping ManyToManyField 'Article.documents'
        db.delete_table('pressroom_article_documents')
        
        # Dropping ManyToManyField 'Article.photos'
        db.delete_table('pressroom_article_photos')
        
        # Dropping ManyToManyField 'Article.sections'
        db.delete_table('pressroom_article_sections')
        
    
    
    models = {
        'pressroom.article': {
            'Meta': {'ordering': "['-pub_date']", 'get_latest_by': "'pub_date'"},
            'author': ('models.CharField', [], {'max_length': '100'}),
            'body': ('models.TextField', ['"Body text"'], {}),
            'documents': ('models.ManyToManyField', ["orm['pressroom.Document']"], {'related_name': "'articles'", 'null': 'True', 'blank': 'True'}),
            'headline': ('models.CharField', [], {'max_length': '200'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'photos': ('models.ManyToManyField', ["orm['photologue.Photo']"], {'related_name': "'articles'", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('models.DateTimeField', ['"Publish date"'], {'default': 'datetime.datetime.now'}),
            'publish': ('models.BooleanField', ['"Publish on site"'], {'default': 'True'}),
            'sections': ('models.ManyToManyField', ["orm['pressroom.Section']"], {'related_name': "'articles'"}),
            'slug': ('models.SlugField', [], {}),
            'summary': ('models.TextField', [], {'blank': 'True'})
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
