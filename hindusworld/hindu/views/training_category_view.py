from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..models import TrainingCategory, TrainingSubCategory
from ..serializers.training_category_serializers import TrainingCategorySerializer
from ..serializers.training_subcategory_serializer import TrainingSubCategorySerializer
from ..utils import CustomPagination


class TrainingCategoryView(viewsets.ModelViewSet):
    # pagination_class = CustomPagination
    queryset = TrainingCategory.objects.all()
    serializer_class = TrainingCategorySerializer
    permission_classes = []

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request):
        filter_kwargs = {key: value for key, value in request.query_params.items()}
        queryset = TrainingCategory.objects.filter(**filter_kwargs)

        if not queryset.exists():
            return Response({
                'message': 'Data not found',
                'status': 404
            }, status=404)

        serialized_data = TrainingCategorySerializer(queryset, many=True)
        return Response(serialized_data.data)
    




    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        # Get the Category by ID
        category = self.get_object()

        # Get all SubCategories related to this Category
        subcategories = TrainingSubCategory.objects.filter(category=category)

        # Serialize SubCategories (returns an empty list if no subcategories are found)
        serialized_data = TrainingSubCategorySerializer(subcategories, many=True).data
        return Response(serialized_data)
