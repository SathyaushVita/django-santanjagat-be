from rest_framework import serializers
from ..models import Training,Register
from ..utils import image_path_to_binary,video_path_to_binary

class TrainingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Training
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['training_link', 'sub_category', 'category', 'training_type', 'video','contact_details','trainer_name','end_date','start_date','location','image','desc','name']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



class TrainingSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Training
        fields = ['status']        







# class TrainerSerializer3(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()
#     video = serializers.SerializerMethodField()
#     certificate = serializers.SerializerMethodField()

#     class Meta:
#         model = Register
#         fields = ["full_name", "image", "video", "location", "status", "certificate",  "user_type", "training_type", "email", "contact_number"]

#     def get_image(self, obj):
#         if obj.image:
#             encoded_image = image_path_to_binary(obj.image)
#             return encoded_image if encoded_image else None
#         return None

#     def get_video(self, obj):
#         if obj.video:
#             encoded_video = video_path_to_binary(obj.video)
#             return encoded_video if encoded_video else None
#         return None

#     def get_certificate(self, obj):
#         if obj.certificate:
#             encoded_certificate = image_path_to_binary(obj.certificate)
#             return encoded_certificate if encoded_certificate else None
#         return None
    




class TrainingSerializer4(serializers.ModelSerializer):
    
                    
    class Meta:
        model = Training
        fields = ['_id','name','image']     



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['name','image']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation









class TrainingSerializer5(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Training
        fields = '__all__' 

    def get_image(self, obj):
        if obj.image:
            encoded_image = image_path_to_binary(obj.image)
            return encoded_image if encoded_image else None
        return None

    def get_video(self, obj):
        if obj.video:
            encoded_video = video_path_to_binary(obj.video)
            return encoded_video if encoded_video else None
        return None
    



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['training_link', 'sub_category', 'category', 'training_type', 'video','contact_details','trainer_name','end_date','start_date','location','image','desc','name']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation
