from urllib.parse import urlparse

from rest_framework import serializers


def youtube_only_validator(value):
    """
    Разрешает только ссылки на youtube.com или youtu.be
    """
    allowed_domains = ["youtube.com", "www.youtube.com", "youtu.be", "www.youtu.be"]
    try:
        parsed = urlparse(value)
        if parsed.scheme not in ["http", "https"]:
            raise serializers.ValidationError(
                "Ссылка должна начинаться с http или https."
            )
        if parsed.netloc not in allowed_domains:
            raise serializers.ValidationError(
                "Можно прикреплять только ссылки на YouTube."
            )
    except Exception:
        raise serializers.ValidationError("Некорректная ссылка.")
