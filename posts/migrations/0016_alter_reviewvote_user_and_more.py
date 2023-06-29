# Generated by Django 4.2.1 on 2023-06-28 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0015_alter_listvote_user_alter_reviewvote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewvote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_votes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='reviewcommentvote',
            unique_together={('user', 'review_comment')},
        ),
        migrations.AlterUniqueTogether(
            name='reviewvote',
            unique_together={('user', 'review')},
        ),
    ]
