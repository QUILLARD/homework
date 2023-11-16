# Generated by Django 4.2 on 2023-11-15 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0002_userprofile_remove_machine_spares_delete_advuser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Сообщение')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='bboard.bb')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send_messages', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
    ]