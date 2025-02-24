# Generated by Django 5.1.6 on 2025-02-24 14:26

import common.kgs
import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.CharField(default=common.kgs.generate_unique_id, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=datetime.datetime(2025, 2, 24, 14, 26, 46, 322097, tzinfo=datetime.timezone.utc))),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('publisher', models.CharField(blank=True, choices=[('Penguin Random House', 'Penguin Random House'), ('HarperCollins', 'HarperCollins'), ('Simon & Schuster', 'Simon & Schuster'), ('Macmillan', 'Macmillan'), ('Village', 'Village'), ('Creative', 'Creative'), ('Other', 'Other')], max_length=255, null=True)),
                ('publication_date', models.DateField()),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('genre', models.CharField(blank=True, choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('Biography', 'Biography'), ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Drama', 'Drama'), ('Family', 'Family'), ('Fantasy', 'Fantasy'), ('History', 'History'), ('Horror', 'Horror'), ('Music', 'Music'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Science Fiction', 'Science Fiction'), ('Thriller', 'Thriller'), ('War', 'War'), ('Western', 'Western')], max_length=100, null=True)),
                ('language', models.CharField(blank=True, choices=[('English', 'English'), ('Hindi', 'Hindi'), ('Marathi', 'Marathi'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu'), ('Kannada', 'Kannada'), ('Malayalam', 'Malayalam'), ('Bengali', 'Bengali'), ('Gujarati', 'Gujarati'), ('Punjabi', 'Punjabi'), ('Urdu', 'Urdu'), ('Other', 'Other')], max_length=50, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='books/')),
                ('sub_category', models.CharField(blank=True, choices=[('Fiction', 'Fiction'), ('Non-fiction', 'Non-fiction'), ('Poetry', 'Poetry'), ('Drama', 'Drama'), ('Comics', 'Comics'), ('Journals', 'Journals'), ('Magazines', 'Magazines'), ('Newspapers', 'Newspapers'), ('Other', 'Other')], max_length=100, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='book_covers/')),
            ],
            options={
                'verbose_name_plural': 'Books',
                'unique_together': {('title', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.CharField(default=common.kgs.generate_unique_id, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('borrow_date', models.DateTimeField(default=datetime.datetime(2025, 2, 24, 14, 26, 46, 324703, tzinfo=datetime.timezone.utc))),
                ('return_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, editable=False)),
                ('is_returned', models.BooleanField(default=False, editable=False)),
                ('is_overdue', models.BooleanField(default=False, editable=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrows', to='library.book')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
