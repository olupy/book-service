from .views import BookViewSet, BorrowBookViewSet

from django.urls import path

app_name = "library"

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrow', BorrowBookViewSet)
urlpatterns = router.urls