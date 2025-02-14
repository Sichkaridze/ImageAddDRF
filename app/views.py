from typing import Type
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from app.models import Message
from app.serializers import (
    MessageSerializer,
    MessageListSerializer,
    MessageDetailSerializer,
    UserSerializer, MessageImageSerializer,
)

class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class MessageListAPI(APIView):
    parser_classes = (MultiPartParser,)

    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        # data_with_user = data.update({"user": user})
        # print(data_with_user)
        data["user"] = user.id
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        message = serializer.save()
        # message.user = user
        # message.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_authenticators(self):
        if self.request.method not in SAFE_METHODS:
            return (TokenAuthentication(),)
        return super().get_authenticators()


class MessageViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        message = self.get_object()
        serializer = self.get_serializer(message, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return MessageListSerializer
        if self.action == "retrieve":
            return MessageDetailSerializer
        if self.action == "upload_image":
            return MessageImageSerializer
        return MessageSerializer

    def perform_create(self, serializer: MessageSerializer) -> Message:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet:
        return Message.objects.filter(user=self.request.user).select_related("user")


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer