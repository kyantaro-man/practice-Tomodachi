# Generated by Django 3.2.4 on 2021-06-12 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friendslist', '0006_friend_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='friendslist.category'),
        ),
    ]
