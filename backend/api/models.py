from django.db import models
from django.contrib.auth.models import User

class JumpVideo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    original_video = models.FileField(upload_to='videos/')
    processed_video = models.FileField(upload_to='processed_videos/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    left_knee_angle = models.FloatField(null=True)
    right_knee_angle = models.FloatField(null=True)
    left_hip_angle = models.FloatField(null=True)
    right_hip_angle = models.FloatField(null=True)
    left_ankle_angle = models.FloatField(null=True)
    right_ankle_angle = models.FloatField(null=True)
    left_shoulder_angle = models.FloatField(null=True)
    right_shoulder_angle = models.FloatField(null=True)
    
    def save(self, *args, **kwargs):
        # Delete old videos when saving new one
        if self.original_video:
            try:
                old_video = JumpVideo.objects.get(user=self.user)
                if old_video.original_video:
                    old_video.original_video.delete()
                if old_video.processed_video:
                    old_video.processed_video.delete()
                old_video.delete()
            except JumpVideo.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Jump Video {self.id} - {self.created_at}"