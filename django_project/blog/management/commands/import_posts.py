from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import json

from django.contrib.auth import get_user_model
from blog.models import Post


class Command(BaseCommand):
    help = 'Import posts from posts.json into the database'

    def handle(self, *args, **options):
        posts_path = Path(settings.BASE_DIR) / 'posts.json'
        if not posts_path.exists():
            self.stderr.write(f'posts.json not found at {posts_path}')
            return

        with posts_path.open(encoding='utf-8') as f:
            data = json.load(f)

        User = get_user_model()
        created = 0
        skipped = 0
        for idx, item in enumerate(data, start=1):
            title = item.get('title') or 'Untitled'
            content = item.get('content') or ''
            user_id = item.get('user_id')

            if user_id is None:
                self.stderr.write(f'Post #{idx} missing user_id; skipping')
                skipped += 1
                continue

            try:
                author = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                # create a dummy user for missing user ids
                username = f'imported_user_{user_id}'
                author, _ = User.objects.get_or_create(
                    username=username,
                    defaults={'email': ''}
                )
                author.set_unusable_password()
                author.save()
                self.stdout.write(f'Created placeholder user `{username}` (id not preserved)')

            Post.objects.create(title=title, content=content, author=author)
            created += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {created} posts'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped {skipped} entries'))
