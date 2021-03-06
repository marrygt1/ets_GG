# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comentarios'
        db.create_table(u'app_comentarios', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Usuario'], null=True)),
            ('grafica', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Graficas'], null=True)),
            ('comentario', self.gf('django.db.models.fields.CharField')(max_length=244)),
            ('calificacion', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'app', ['Comentarios'])

        # Deleting field 'Usuario.curso'
        db.delete_column(u'app_usuario', 'curso_id')


    def backwards(self, orm):
        # Deleting model 'Comentarios'
        db.delete_table(u'app_comentarios')

        # Adding field 'Usuario.curso'
        db.add_column(u'app_usuario', 'curso',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Curso'], null=True, blank=True),
                      keep_default=False)


    models = {
        u'app.comentarios': {
            'Meta': {'object_name': 'Comentarios'},
            'calificacion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comentario': ('django.db.models.fields.CharField', [], {'max_length': '244'}),
            'grafica': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Graficas']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Usuario']", 'null': 'True'})
        },
        u'app.curso': {
            'Meta': {'object_name': 'Curso'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        },
        u'app.graficas': {
            'Meta': {'object_name': 'Graficas'},
            'curso': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Curso']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'administrador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '50'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'perfil': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'usuario': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35', 'db_index': 'True'})
        },
        u'app.valores': {
            'Meta': {'object_name': 'Valores'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '40'}),
            'grafica': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Graficas']", 'null': 'True'}),
            'highlight': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'value': ('django.db.models.fields.FloatField', [], {'max_length': '40'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']