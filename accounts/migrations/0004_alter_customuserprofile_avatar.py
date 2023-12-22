# Generated by Django 4.1.3 on 2023-12-22 14:12

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_subscriber_email_alter_subscriber_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.utils.avatar_upload_to),
        ),
    ]