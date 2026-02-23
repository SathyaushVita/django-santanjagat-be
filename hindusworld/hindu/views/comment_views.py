
from rest_framework import viewsets
from ..models import *
from rest_framework .response import Response
from ..serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.timesince import timesince

class CommentView(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()


    for comment in queryset:
        if comment.created_at:
            comment.posted_time_ago = f"{timesince(comment.created_at)} ago"
            comment.save()