from django.conf import settings
from django.db import models


class Message(models.Model):
    TEXT_PREVIEW_LEN = 20
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")
    image = models.ImageField(null=True, upload_to="uploads/")

    @property
    def text_preview(self) -> str:
        return (
            self.text
            if len(self.text) < Message.TEXT_PREVIEW_LEN
            else self.text[:Message.TEXT_PREVIEW_LEN] + "..."
        )