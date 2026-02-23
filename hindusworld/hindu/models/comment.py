import uuid
from django.db import models
from . import *
from .user import Register
# from .temple import Temple
# from .goshala import Goshala
from django.utils.timesince import timesince
from .event import Event
import uuid
from django.db import models
from django.utils import timezone

class CommentModel(models.Model):
    _id = models.UUIDField(db_column='_id', primary_key=True, default=uuid.uuid4, editable=False)
    # temple = models.ForeignKey(Temple, db_column="temple", on_delete=models.CASCADE, related_name='comments', blank=True, null=True) 
    user = models.ForeignKey(Register, db_column="user", on_delete=models.CASCADE, related_name='comments', blank=True, null=True) 
    # goshala = models.ForeignKey(Goshala, db_column="goshala", on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    event = models.ForeignKey(Event, db_column="event", on_delete=models.CASCADE, related_name='comments', blank=True, null=True) 
    body = models.CharField(db_column='body', max_length=(5000))
    created_at = models.DateTimeField(auto_now_add=True)
    posted_time_ago = models.CharField(db_column='posted_time_ago', max_length=255,blank=True)
    

    @property
    def relative_time(self):
        return timesince(self.created_at, timezone.now())
    

    class Meta:
        managed = True
        db_table = 'comment'
        ordering = ['-created_at'] 

