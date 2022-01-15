# Generated by Django 3.1.14 on 2022-01-15 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20220113_1728'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tagrecipe',
            constraint=models.UniqueConstraint(fields=('tag', 'recipe'), name='unique tag for recipe'),
        ),
    ]
