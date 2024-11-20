# Generated by Django 5.1.3 on 2024-11-19 13:19

import api.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('stock', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('borrow_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('borrow_at', models.DateTimeField(auto_now_add=True)),
                ('return_deadline', models.DateTimeField(default=api.models.default_return_deadline)),
                ('books', models.ManyToManyField(related_name='borrowed_books', to='api.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('fine_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('borrow', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fine', to='api.borrow')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fines', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]