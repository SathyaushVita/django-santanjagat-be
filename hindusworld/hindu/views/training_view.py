from rest_framework import viewsets, generics, status
from ..models import Training,Register
from ..serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_azure,image_path_to_binary,video_path_to_binary,save_video_to_azure
import uuid
import os
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework import viewsets, pagination
from datetime import datetime
from rest_framework import status as http_status
from ..enums import status


class CustomPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100




from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings



class TrainingView(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Fetch the Register instance for the logged-in user
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            user_type = register_instance.user_type

            # Check if the user type is ADMIN
            if user_type != "ADMIN":
                return Response({
                    "message": "Only ADMIN users can create training records."
                }, status=status.HTTP_403_FORBIDDEN)

            # Capture the current time
            created_at = timezone.now()

            # Proceed with training session creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            # Process image
            image_data = request.data.get('image')
            if image_data and image_data != "null":
                saved_image_location = save_image_to_azure(image_data, instance._id, instance.name, 'trainings')
                if saved_image_location:
                    # No need to split the URL, just save the full path
                    instance.image = saved_image_location
                    instance.save()

            # Process video
            video_data = request.data.get('video')
            if video_data and video_data != "null":
                saved_video_location = save_video_to_azure(video_data, instance._id, instance.name, 'trainings')
                if saved_video_location:
                    # No need to split the URL, just save the full path
                    instance.video = saved_video_location
                    instance.save()

            # Send email notification
            send_mail(
                'New Training Session Added',
                f'User ID: {request.user.id}\n'
                f'Contact Number: {register_instance.contact_number}\n'
                # f'Full Name: {request.user.get_full_name()}\n'
                f'Training ID: {instance._id}\n'
                f'Training Name: {instance.name}\n'
                f'Created At: {created_at.strftime("%Y-%m-%d %H:%M:%S")}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # Return successful response with correct paths
            return Response({
                "message": "Training session added successfully.",
                "result": {
                    **serializer.data,
                    "image": instance.image,
                    "video": instance.video
                }
            }, status=status.HTTP_201_CREATED)

        except Register.DoesNotExist:
            return Response({
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def list(self, request, *args, **kwargs):
        try:
            # Filter queryset to include only items with status SUCCESS
            queryset = self.get_queryset().filter(status='SUCCESS')
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            for item in data:
                image_path = item.get('image')
                video_path = item.get('video')

                if image_path and image_path != "null":
                    # Ensure the URL is complete
                    item['image'] = image_path if image_path.startswith('http') else os.path.join(settings.FILE_URL, image_path)

                if video_path and video_path != "null":
                    # Ensure the URL is complete
                    item['video'] = video_path if video_path.startswith('http') else os.path.join(settings.FILE_URL, video_path)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            is_admin = register_instance.user_type == "ADMIN"

            if not is_admin:
                return Response({
                    "message": "Only admin users can update training sessions."
                }, status=status.HTTP_403_FORBIDDEN)

            data = request.data
            image_data = data.get('image')
            video_data = data.get('video')

            _id = str(uuid.uuid4())
            name = data.get('name', 'default_name')

            if image_data:
                image_path = save_image_to_azure(image_data, _id, name, 'trainings')
                if image_path:
                    data['image'] = image_path

            if video_data:
                video_path = save_video_to_azure(video_data, _id, name, 'trainings')
                if video_path:
                    data['video'] = video_path

            serializer = TrainingSerializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            return Response({
                "message": "Training session updated successfully.",
                "data": TrainingSerializer(updated_instance).data
            }, status=status.HTTP_200_OK)

        except Training.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

        except Register.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






    def retrieve(self, request, *args, **kwargs):
        try:
            # Retrieve the object by ID and ensure status is SUCCESS
            instance = self.get_queryset().filter(_id=kwargs.get('pk'), status='SUCCESS').first()

            if not instance:
                return Response({
                    "message": "Item not found or status is not SUCCESS."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(instance)
            data = serializer.data

            # Construct image and video URLs
            image_path = data.get('image')
            video_path = data.get('video')

            if image_path and image_path != "null":
                # Ensure the URL is complete
                data['image'] = image_path if image_path.startswith('http') else os.path.join(settings.FILE_URL, image_path)

            if video_path and video_path != "null":
                # Ensure the URL is complete
                data['video'] = video_path if video_path.startswith('http') else os.path.join(settings.FILE_URL, video_path)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class UpdateTrainingStatus(generics.GenericAPIView):
    serializer_class = TrainingSerializer2

    def put(self, request, training_id):
        try:
            training = Training.objects.get(pk=training_id, status='PENDING')
        except Training.DoesNotExist:
            return Response({
                'message': 'Training with PENDING status not found for the provided ID'
            }, status=status.HTTP_404_NOT_FOUND)

        # Update the status to 'SUCCESS'
        training.status = 'SUCCESS'
        training.save()

        # Serialize the updated training
        serializer = self.get_serializer(training)

        return Response({
            'message': 'success',
            'result': serializer.data
        }, status=status.HTTP_200_OK)



class GetTrainingsByLocation(generics.ListAPIView):
    serializer_class = TrainingSerializer5  
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        sub_category = self.request.query_params.get('sub_category')

        # Validate that at least one of the filters is provided
        if not input_value and not category and not sub_category:
            raise ValidationError("At least one of 'input_value', 'category', or 'sub_category' is required.")

        # Start with all Training objects
        queryset = Training.objects.all()

        # Check input_value against location hierarchy
        if input_value:
            queryset = queryset.filter(
                Q(object_id__state__country__continent__pk=input_value) |
                Q(object_id__state__country__pk=input_value) |
                Q(object_id__state__pk=input_value) |
                Q(object_id__pk=input_value)
            )

        # Apply category filtering if provided
        if category:
            queryset = queryset.filter(
                Q(category_id=category) | Q(sub_category_id=category)
            )

        # Apply sub-category filtering if provided
        if sub_category:
            queryset = queryset.filter(sub_category_id=sub_category)

        # Filter by status
        queryset = queryset.filter(status='SUCCESS')  # Adjust this to your actual status field

        # Order by '_id' to ensure compatibility with pagination
        queryset = queryset.order_by('_id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)