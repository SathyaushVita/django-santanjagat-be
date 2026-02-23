from rest_framework import viewsets, generics
from ..models import TrainingSubCategory
from ..serializers.training_subcategory_serializer import TrainingSubCategorySerializer
from ..utils import CustomPagination


class TrainingSubCategoryView(viewsets.ModelViewSet):
    # pagination_class = CustomPagination
    queryset = TrainingSubCategory.objects.all()
    serializer_class = TrainingSubCategorySerializer