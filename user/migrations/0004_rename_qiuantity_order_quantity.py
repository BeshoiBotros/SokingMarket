# Generated by Django 4.2.1 on 2023-05-26 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_item_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='qiuantity',
            new_name='quantity',
        ),
    ]
