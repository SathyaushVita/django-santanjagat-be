from rest_framework import serializers
from ..models import SubCategory
from ..serializers import CategorySerializer
from ..utils import image_path_to_binary




class SubCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, instance):

            filename = instance.image
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None
    class Meta:
        model = SubCategory
        fields = '__all__'