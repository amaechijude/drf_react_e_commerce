from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="email already taken")]
        )
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        if not str(value).strip().endswith("@unn.edu.ng"):
            raise serializers.ValidationError("You are not a unn student")
        return value
    
    def validate(self, attrs):
        password1 = attrs["password"]
        password2 = attrs.get("confirm_password")
        
        if len(password1) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")

        if password1 != password2:
            raise serializers.ValidationError("Password mismatch")

        if not any(char.isupper() for char in password1):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")

        # Check for lowercase letter
        if not any(char.islower() for char in password1):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")

        # Check for digit
        if not any(char.isdigit() for char in password1):
            raise serializers.ValidationError("Password must contain at least one number")

        # Check for special character
        special_characters = r"!@#$%^&*()-_=+[]{}|;:',.<>?/`~"
        if not any(char in special_characters for char in password1):
            raise serializers.ValidationError("Password must contain at least one special character")
        
        attrs.pop("confirm_password", None)
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
