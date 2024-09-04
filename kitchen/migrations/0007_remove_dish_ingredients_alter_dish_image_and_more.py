# Generated by Django 5.0.7 on 2024-09-03 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0006_alter_ingredient_options_alter_cook_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='ingredients',
        ),
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(default='', upload_to='dish_images'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DishIngredient',
        ),
    ]