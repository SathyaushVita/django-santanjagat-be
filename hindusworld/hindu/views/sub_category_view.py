from rest_framework import viewsets, generics
from ..models import SubCategory
from ..serializers.sub_category_serializer import SubCategorySerializer
from ..utils import CustomPagination



class SubCategoryView(viewsets.ModelViewSet):
    # pagination_class = CustomPagination
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer