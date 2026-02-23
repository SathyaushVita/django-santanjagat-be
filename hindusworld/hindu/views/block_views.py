from rest_framework import viewsets
from ..models import Block
from ..serializers import BlockSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework .response import Response

class BlockView(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in [ 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()


    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = Block.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = BlockSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Block.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })