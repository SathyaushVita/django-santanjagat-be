from django.db import models
from .training_category import TrainingCategory
import uuid

class TrainingSubCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False)
    name = models.CharField(db_column='name', max_length=200) 
    desc=models.CharField(db_column='desc',max_length=10000)
    category = models.ForeignKey(TrainingCategory, on_delete=models.SET_NULL, db_column='category', null=True, blank=True)
    image = models.TextField(null=True,blank=True)

    



    class Meta:
        managed=False
        db_table = 'training_subcategory'