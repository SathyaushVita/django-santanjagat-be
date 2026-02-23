import uuid
from django.db import models
from ..models import *
# from .goshala import Goshala

from django.contrib.contenttypes.fields import GenericRelation
from .district import District


class Block(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    municipality = models.CharField(db_column='municipality', max_length=45, blank=True, null=True)
    population = models.CharField(db_column='population', max_length=45, blank=True, null=True)
    desc = models.CharField(db_column='desc', max_length=2500)  
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='blocks')   
    created_at = models.DateTimeField(auto_now_add=True)
    type=models.CharField(db_column='type', max_length=30, choices=[('BLOCK','BLOCK'),('TOWN','TOWN')],default='BLOCK',blank=True)
    

    class Meta:
        managed = True
        db_table = 'block'
