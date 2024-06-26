# Generated by Django 4.2.1 on 2023-05-28 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_name_reviewer_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default='default@email.com', max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
