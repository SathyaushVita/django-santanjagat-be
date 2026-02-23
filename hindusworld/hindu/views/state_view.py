from ..models import State,Country
from ..serializers import StateSeerializer
from rest_framework import viewsets
from rest_framework .response import Response
from rest_framework import generics,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..utils import CustomPagination



class StateViews(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = State.objects.all()
    serializer_class = StateSeerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'country__name']  # Ensure these fields are valid in your model

    def list(self, request):
        filter_kwargs = {}
        
        # Filter only with valid fields
        for key, value in request.query_params.items():
            if key in ['name', 'country']:  # Adjust based on actual model fields
                filter_kwargs[key] = value

        try:
            queryset = State.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serialized_data = StateSeerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class states_by_country(generics.GenericAPIView):
    serializer_class = StateSeerializer

    def get(self, request, country):
        try:
            # Fetch the continent using the provided ID
            country = State.objects.filter(country=country)

            serialized_data=StateSeerializer(country,many=True)

            state_count = country.count()

           
            return Response({
                "state_count": state_count,
                "states": serialized_data.data
            }, status=status.HTTP_200_OK)
        
        except Country.DoesNotExist:
            return Response({
                'message': 'Country not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

