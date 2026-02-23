from django.db import models
import uuid
from ..enums.user_type_enum import UserType
from ..enums import TrainingType
from .user import Register




class TrainerUser(models.Model):
    training_type = models.CharField(db_column='training_type',max_length=10,choices=[(e.value, e.value) for e in TrainingType],default=TrainingType.OFFLINE.value) 
    certificate = models.TextField(db_column='certificate',null=True,blank=True)
    user_type = models.CharField(db_column='user_type',max_length=45, choices=[(e.name, e.value)for e in UserType], default=UserType.MEMBER.value)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='trainer_users', null=True)






    class Meta:
        managed=False
        db_table = 'trainer_user'


 



    
