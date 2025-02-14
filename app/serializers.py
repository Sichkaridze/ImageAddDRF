from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.models import Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):
        user = get_user_model()(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Message
        fields = ("id", "text", "created_at", "image", "user")

    # def create(self, validated_data):
    #     foo = Message.objects.create(
    #         user=self.context['request'].user,
    #         **validated_data
    #     )
    #     return foo






class MessageListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    image = serializers.ImageField(read_only=True)
    class Meta:
        model = Message
        fields = ("id", "text_preview", "created_at", "user", "user_username", "image")


class MessageDetailSerializer(MessageSerializer):
    user = UserSerializer(many=False)


class MessageImageSerializer(serializers.ModelSerializer):
   class Meta:
       model = Message
       fields = ("id", "image",)
