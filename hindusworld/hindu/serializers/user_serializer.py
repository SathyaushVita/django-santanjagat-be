from rest_framework import serializers
from ..models import Register
from ..utils import image_path_to_binary
from ..serializers.organization_serializer import OrgnisationSerializer
# from .event_serializer import EventsSerializer1
from ..serializers.training_serializers import TrainingSerializer5
from ..serializers.event_serializer import EventSerializer1


class Register_LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username"]
      

class Verify_LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username","verification_otp"]


class MemberSerializer(serializers.ModelSerializer):
    Organization  = OrgnisationSerializer(many=True, read_only=True) 
    events = EventSerializer1(many=True, read_only=True)
    Training=TrainingSerializer5(many=True, read_only=True)

    
    class Meta:
        model=Register
        fields=["id","full_name","father_name","profile_pic","gender","contact_number","is_member", "certificate", "user_type", "email","Organization","Training","events","surname"]


class MemberPicSerializer(serializers.ModelSerializer):
    profile_pic=serializers.SerializerMethodField()
    def get_profile_pic(self, instance):
        filename = instance.profile_pic
        if filename:
            format = image_path_to_binary(filename)
            return format
        return []
    class Meta:
        model = Register
        fields = "__all__"


