from typing import Optional

from rest_framework import serializers
from library.producer import send_kafka_event
from library.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at","is_available")

    def create(self, validated_data):
        book: Book = super().create(validated_data)
        book_event_data: dict[str, Optional[str]] = {
            "id": str(book.id),
            "title": book.title,
            "author": book.author,
            "publication_date": book.publication_date.isoformat() if book.publication_date else None,
            "isbn": book.isbn,
            "is_available": book.is_available,
            "event": "BOOK_CREATED",
            "genre": book.genre,
            "language": book.language,
            "sub_category": book.sub_category,
            "publisher": book.publisher,
            "file": book.file.url if book.file else None,
            "cover_image": book.cover_image.url if book.cover_image else None
        }
        send_kafka_event("book_created_topic", book_event_data)
        return book


class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "isbn", "is_available")
        read_only_fields = ("id", "title", "author", "isbn", "is_available")
