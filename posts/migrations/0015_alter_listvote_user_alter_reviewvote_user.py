# Generated by Django 4.2.1 on 2023-06-28 21:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0014_alter_listvote_user_alter_reviewvote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listvote',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='list_vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reviewvote',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review_vote', to=settings.AUTH_USER_MODEL),
        ),
    ]
