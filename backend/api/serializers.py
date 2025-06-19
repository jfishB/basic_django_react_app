from django.contrib.auth.models import User
from rest_framework import serializers
from .models import JumpVideo

# converts python objects into json equivalent and vice versa

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class JumpVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = JumpVideo
        fields = ['id', 'original_video', 'processed_video', 'created_at', 
                 'left_knee_angle', 'right_knee_angle', 
                 'left_hip_angle', 'right_hip_angle',
                 'left_ankle_angle', 'right_ankle_angle',
                 'left_shoulder_angle', 'right_shoulder_angle']
        read_only_fields = ['processed_video', 'left_knee_angle', 'right_knee_angle',
                           'left_hip_angle', 'right_hip_angle',
                           'left_ankle_angle', 'right_ankle_angle',
                           'left_shoulder_angle', 'right_shoulder_angle']