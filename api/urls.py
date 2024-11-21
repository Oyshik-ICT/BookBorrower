from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

router = DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")
router.register(r"borrows", views.BorrowViewSet, basename="borrow")
router.register(r"fines", views.FineViewSet, basename="fine")

urlpatterns = [
    path("", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
