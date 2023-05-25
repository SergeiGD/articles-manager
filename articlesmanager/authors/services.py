from django.utils import timezone


def delete_author(author):
    author.date_deleted = timezone.now()
    author.save()
