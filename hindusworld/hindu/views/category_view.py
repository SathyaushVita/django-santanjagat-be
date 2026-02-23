from rest_framework import viewsets, generics
from ..models import Category,SubCategory
from ..serializers.category_serializer import CategorySerializer
from ..serializers.sub_category_serializer import SubCategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..utils import CustomPagination



class CategoryView(viewsets.ModelViewSet):
    # pagination_class = CustomPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        # Get the Category by ID
        category = self.get_object()

        # Get all SubCategories related to this Category
        subcategories = SubCategory.objects.filter(category_id=category)

        # Serialize SubCategories
        serialized_data = SubCategorySerializer(subcategories, many=True).data

        # Return the list of SubCategory data in the response
        return Response(serialized_data)