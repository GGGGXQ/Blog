# Generated by Django 5.1.3 on 2024-11-26 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_user_friends_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="posts_count",
            field=models.IntegerField(default=0),
        ),
    ]