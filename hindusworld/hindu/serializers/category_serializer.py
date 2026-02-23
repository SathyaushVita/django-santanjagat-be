from rest_framework import serializers
from ..models import Category
from ..utils import image_path_to_binary




class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, instance):

            filename = instance.image
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None
    class Meta:
        model = Category
        fields = "__all__"