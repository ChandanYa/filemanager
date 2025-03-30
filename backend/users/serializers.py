from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country', 'is_default']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'phone_number',
            'password',
            'password_confirmation',
            'addresses'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': 'Passwords do not match'
            })
        
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
            
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password']
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        style={'input_type': 'password'},
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'phone_number',
            'current_password',
            'new_password'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'phone_number': {'required': False},
        }

    def validate(self, data):
        if 'new_password' in data and 'current_password' not in data:
            raise serializers.ValidationError({
                'current_password': 'Current password is required to set a new password'
            })
        return data

    def update(self, instance, validated_data):
        if 'new_password' in validated_data:
            if not instance.check_password(validated_data['current_password']):
                raise serializers.ValidationError({
                    'current_password': 'Current password is incorrect'
                })
            instance.set_password(validated_data['new_password'])
        
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country', 'is_default']
        extra_kwargs = {
            'is_default': {'required': False, 'default': False}
        }

    def validate(self, data):
        # Add any custom address validation here
        return data