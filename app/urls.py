from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from DjangoProject import settings
from app.views import MessageViewSet, UserViewSet, CreateTokenView, MessageListAPI

router = DefaultRouter()

# router.register("messages", MessageViewSet, basename="messages")
router.register("users", UserViewSet)

urlpatterns = [
    path('messages/', MessageListAPI.as_view(), name='messages-list'),
    path("", include(router.urls)),
    path("login/", CreateTokenView.as_view(), name="token"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "messenger"