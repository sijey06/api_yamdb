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
                Category.objects.update_or_create(id=row['id'], defaults=row)
            elif model_name == 'genres':
                Genre.objects.update_or_create(id=row['id'], defaults=row)
            elif model_name == 'users':
                UserProfile.objects.update_or_create(
                    id=row['id'], defaults=row
                )
            elif model_name == 'titles':
                category_id = row.pop('category')
                category = Category.objects.get(id=category_id)
                Title.objects.update_or_create(
                    id=row['id'], defaults={**row, 'category': category}
                )
            elif model_name == 'genre_title':
                title_id = row['title_id']
                genre_id = row['genre_id']
                title = Title.objects.get(id=title_id)
                genre = Genre.objects.get(id=genre_id)
                title.genre.add(genre)
            elif model_name == 'reviews':
                author_id = row.pop('author')
                title_id = row.pop('title_id')
                author = UserProfile.objects.get(id=author_id)
                title = Title.objects.get(id=title_id)
                Review.objects.update_or_create(
                    id=row['id'],
                    defaults={**row, 'author': author, 'title': title},
                )
            elif model_name == 'comments':
                author_id = row.pop('author')
                review_id = row.pop('review_id')
                review = Review.objects.get(id=review_id)
                Comment.objects.update_or_create(
                    id=row['id'],
                    defaults={**row, 'author_id': author_id, 'review': review},
                )
