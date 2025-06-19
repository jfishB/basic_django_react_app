from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, JumpVideoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import JumpVideo
from .mediapipe_pose import run_mediapipe_pose
import os
from django.conf import settings

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class JumpVideoViewSet(generics.ListCreateAPIView):
    serializer_class = JumpVideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return JumpVideo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        video = serializer.save(user=self.request.user)
        
        input_path = os.path.join(settings.MEDIA_ROOT, str(video.original_video))
        output_path = os.path.join(settings.MEDIA_ROOT, 'processed_videos', f'processed_{os.path.basename(str(video.original_video))}')
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        max_angles = run_mediapipe_pose(input_path, output_path)
        
        video.processed_video = f'processed_videos/processed_{os.path.basename(str(video.original_video))}'
        video.left_knee_angle = max_angles['left_knee']
        video.right_knee_angle = max_angles['right_knee']
        video.left_hip_angle = max_angles['left_hip']
        video.right_hip_angle = max_angles['right_hip']
        video.left_ankle_angle = max_angles['left_ankle']
        video.right_ankle_angle = max_angles['right_ankle']
        video.save()