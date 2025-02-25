from datetime import timezone

from django.db import models
from common.models import AuditableModel
from .enums import GenreEnum, LanguageEnum, SubCategoryEnum, PublisherEnum
from user.models import User
from django.utils import timezone
# Create your models here.

class Book(AuditableModel):

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    publisher = models.CharField(max_length=255, null = True, blank = True, choices= PublisherEnum.choices()) # used enums for now... it should be dynamic as any publisher can easily be created. TODO: remove this
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100, null = True, blank = True, choices= GenreEnum.choices())
    language = models.CharField(max_length=50, null = True, blank = True, choices= LanguageEnum.choices())
    file = models.FileField(upload_to='books/', null=True, blank=True)
    sub_category = models.CharField(max_length=100, null = True, blank = True, choices= SubCategoryEnum.choices())
    is_available = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name_plural = 'Books'
        unique_together = ('title', 'author')



class Borrow(AuditableModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books", null = True)
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, editable=False)
    is_returned = models.BooleanField(default=False, editable=False)
    is_overdue = models.BooleanField(default=False, editable=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.user} borrowed {self.book}"

