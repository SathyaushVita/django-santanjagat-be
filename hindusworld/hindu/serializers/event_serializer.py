# from rest_framework import serializers
# from ..models import Events
# from ..utils import image_path_to_binary

# class EventsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Events
#         fields = "__all__"






# class EventsSerializer1(serializers.ModelSerializer):
#     brochure = serializers.SerializerMethodField()
#     event_images = serializers.SerializerMethodField()  
#     relative_time = serializers.SerializerMethodField()


#     def get_brochure(self, instance):
#         if instance.brochure:
#             return image_path_to_binary(instance.brochure)
#         return None

#     def get_event_images(self, instance):
#         # Return only the first image if available
#         if instance.event_images:
#             first_image = instance.event_images[0] if instance.event_images else None
#             return image_path_to_binary(first_image) if first_image else None
#         return None
    
#     def get_relative_time(self, obj):
#         return obj.relative_time

#     class Meta:
#         model = Events
#         fields = '__all__'


#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         # Fields to check for empty or null values
#         fields_to_check = ['event_details', 'event_status', 'category', 'live_stream_link','event_images','contact_details','end_date','start_date','location','organizer_name','brochure','name']
#         for field in fields_to_check:
#             if representation.get(field) in [None, '', 'null','-']:
#                 representation[field] = "data not found"
  
#         return representation



# class EventSerializer2(serializers.ModelSerializer):
    
#     class Meta:
#         model = Events
#         fields = ['status']        







# class EventsSerializer3(serializers.ModelSerializer):
#     event_image = serializers.SerializerMethodField()  # Renaming to event_image for single image

#     def get_event_image(self, instance):
#         # Return only the first image if available
#         if instance.event_images:
#             first_image = instance.event_images[0] if instance.event_images else None
#             return image_path_to_binary(first_image) if first_image else None
#         return None

#     class Meta:
#         model = Events
#         fields = ['_id', 'event_image', 'name']


#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         # Fields to check for empty or null values
#         fields_to_check = ['event_image', 'name']
#         for field in fields_to_check:
#             if representation.get(field) in [None, '', 'null','-']:
#                 representation[field] = "data not found"
  
#         return representation









from rest_framework import serializers
from ..models.event import Event
from ..utils import image_path_to_binary
from ..serializers.comment_serializer import CommentSerializer12


from rest_framework import serializers
from ..models.event import Event
from ..utils import image_path_to_binary
from ..serializers.comment_serializer import CommentSerializer12
from django.conf import settings
import json


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {
                'image_location': {'required': False, 'default': list}
            }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image_location:
            # Process `image_location` as a list, converting any stored strings to list format
            image_locations = (
                instance.image_location
                if isinstance(instance.image_location, list)
                else instance.image_location.strip('[]').replace('"', '').split(',')
            )
            image_locations = [f"{settings.FILE_URL}{path.strip()}" for path in image_locations]
            representation['image_location'] = image_locations
        else:
            representation['image_location'] = []
        return representation
class EventSerializer1(serializers.ModelSerializer):
    comments = CommentSerializer12(many=True)
    image_location = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()
    def get_image_location(self, instance):
        filenames = instance.image_location
        if filenames:
            # Handle the case where image_location is a list
            if isinstance(filenames, list):
                # Convert each path to binary format
                return [image_path_to_binary(filename) for filename in filenames]
            else:
                # If it's a single string, just convert that one
                return [image_path_to_binary(filenames)]
        return []
    def get_relative_time(self, obj):
        return obj.relative_time
    class Meta:
        model = Event
        fields = "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure image_location is returned as a list of full URLs
        if instance.image_location:
            if isinstance(instance.image_location, str):
                # If it's a string, treat it as a list of paths (handling the old format)
                image_locations = instance.image_location.strip('[]').replace('"', '').split(',')
                image_locations = [path.strip() for path in image_locations]
            elif isinstance(instance.image_location, list):
                # If it's already a list, clean it up
                image_locations = [path.strip() for path in instance.image_location if isinstance(path, str)]
            else:
                image_locations = []
            # Prepend the base FILE_URL to each image path
            image_locations = [f"{settings.FILE_URL}{path}" for path in image_locations]
            representation['image_location'] = image_locations
        else:
            representation['image_location'] = []
        return representation






class EventsSerializer3(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    def get_image_location(self, instance):

            filename = instance.image_location
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None

    class Meta:
        model = Event
        fields = ['_id', 'image_location', 'name']