# Generated by Django 4.2.1 on 2023-05-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='items/images/default.jpg', upload_to='items/images/%y/%m/%d/%H/%M/%S'),
        ),
    ]