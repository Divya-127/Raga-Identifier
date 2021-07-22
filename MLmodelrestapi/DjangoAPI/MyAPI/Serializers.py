from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    audio = serializers.FileField(max_length=None,use_url=True)

    class Meta:
        model = Task
        fields = "__all__"