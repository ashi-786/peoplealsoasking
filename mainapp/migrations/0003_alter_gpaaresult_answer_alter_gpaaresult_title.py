# Generated by Django 5.2 on 2025-05-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_gpaaresult_title_alter_gpaaresult_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpaaresult',
            name='answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gpaaresult',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
