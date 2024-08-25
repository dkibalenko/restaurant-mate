# Generated by Django 5.0.7 on 2024-08-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0005_cook_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='cook',
            name='profile_picture',
            field=models.ImageField(default='profile_images/dennie_smile.jpeg', upload_to='profile_images'),
            preserve_default=False,
        ),
    ]
