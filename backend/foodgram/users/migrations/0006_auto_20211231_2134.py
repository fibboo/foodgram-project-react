# Generated by Django 3.1.14 on 2021-12-31 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20211225_1837'),
        ('users', '0005_auto_20211228_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipes',
            field=models.ManyToManyField(related_name='shopping_cart', through='users.ShoppingCartRecipe', to='recipes.Recipe', verbose_name='Ingredients'),
        ),
    ]
