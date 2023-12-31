# Generated by Django 4.2.2 on 2023-07-19 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('subscribers', models.ManyToManyField(related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(choices=[('AR', 'Статья'), ('NE', 'Новость')], default='NE', max_length=2)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('textPost', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News_from_Ozersk.author1')),
            ],
        ),
        migrations.CreateModel(
            name='NewCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News_from_Ozersk.category')),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='News_from_Ozersk.new')),
            ],
        ),
        migrations.AddField(
            model_name='new',
            name='category',
            field=models.ManyToManyField(through='News_from_Ozersk.NewCategory', to='News_from_Ozersk.category'),
        ),
    ]
