# Generated by Django 5.0.3 on 2024-04-28 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0002_rename_knowledgesetmodel_knowledgeinfomodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='KnowledgeInfoModel',
            new_name='KnowledgeInfo',
        ),
    ]