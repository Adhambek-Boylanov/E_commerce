from rest_framework import serializers

class SendSmsSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    verify_kod = serializers.CharField(max_length=6)
