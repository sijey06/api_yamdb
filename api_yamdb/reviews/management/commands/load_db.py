import os
import csv

from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage

from reviews.models import Genre, Category, Title, Review, Comment
from users.models import UserProfile

DATA_DIR = 'static/data/'
FILES = {
    'categories': 'category.csv',
    'genres': 'genre.csv',
    'users': 'users.csv',
    'titles': 'titles.csv',
    'genre_title': 'genre_title.csv',
    'reviews': 'review.csv',
    'comments': 'comments.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в базу данных.'

    def handle(self, *args, **options):
        for model_name, filename in FILES.items():
            full_path = os.path.join(DATA_DIR, filename)
            if not default_storage.exists(full_path):
                self.stderr.write(
                    self.style.ERROR(f'Файл "{full_path}" не существует.')
                )
                continue

            self.stdout.write(
                self.style.SUCCESS(f'Загрузка данных из {filename}...')
            )
            with open(full_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.load_model(model_name, reader)

        self.stdout.write(self.style.SUCCESS('Все данные загружены успешно!'))

    def load_model(self, model_name, reader):
        for row in reader:
            if model_name == 'categories':
                self.load_category(row)
            elif model_name == 'genres':
                self.load_genre(row)
            elif model_name == 'users':
                self.load_user(row)
            elif model_name == 'titles':
                self.load_title(row)
            elif model_name == 'genre_title':
                self.load_genre_title(row)
            elif model_name == 'reviews':
                self.load_review(row)
            elif model_name == 'comments':
                self.load_comment(row)

    def load_category(self, row):
        Category.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'slug': row['slug'],
            },
        )

    def load_genre(self, row):
        Genre.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'slug': row['slug'],
            },
        )

    def load_user(self, row):
        UserProfile.objects.update_or_create(
            id=row['id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'username': row['username'],
                'bio': row['bio'],
                'email': row['email'],
                'role': row['role'],
            },
        )

    def load_title(self, row):
        category_id = row.pop('category')
        category = Category.objects.get(id=category_id)
        Title.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row['name'],
                'year': row['year'],
                'category': category,
            },
        )

    def load_genre_title(self, row):
        title_id = row['title_id']
        genre_id = row['genre_id']
        title = Title.objects.get(id=title_id)
        genre = Genre.objects.get(id=genre_id)
        title.genre.add(genre)

    def load_review(self, row):
        author_id = row.pop('author')
        title_id = row.pop('title_id')
        author = UserProfile.objects.get(id=author_id)
        title = Title.objects.get(id=title_id)
        Review.objects.update_or_create(
            id=row['id'],
            defaults={
                'text': row['text'],
                'score': row['score'],
                'author': author,
                'title': title,
                'pub_date': row['pub_date'],
            },
        )

    def load_comment(self, row):
        author_id = row.pop('author')
        review_id = row.pop('review_id')
        review = Review.objects.get(id=review_id)
        Comment.objects.update_or_create(
            id=row['id'],
            defaults={
                'text': row['text'],
                'author_id': author_id,
                'review': review,
                'pub_date': row['pub_date'],
            },
        )
