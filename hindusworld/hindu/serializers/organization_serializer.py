from rest_framework import serializers
from ..models import Organization
from ..utils import image_path_to_binary



class OrgnisationSerializer(serializers.ModelSerializer):
    org_images = serializers.SerializerMethodField()
    org_logo = serializers.SerializerMethodField()
    # govt_id_proof = serializers.SerializerMethodField()  

    def get_org_images(self, instance):
        filename = instance.org_images
        if filename:
            format = image_path_to_binary(filename)
            return format
        return []

    def get_org_logo(self, instance):
        filename = instance.org_logo
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    # def get_govt_id_proof(self, instance):
    #     filename = instance.govt_id_proof
    #     if filename:
    #         format = image_path_to_binary(filename)
    #         return format
    #     return None

    class Meta:
        model = Organization
        fields = '__all__'
    


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members','sub_category_id','object_id']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



       
    class Meta:
        model = Organization
        fields = "__all__"



    
    
class OrgnisationSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = "__all__"



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members','sub_category_id','object_id']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



class OrgnisationSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = ['status']        

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members','sub_category_id','object_id']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation






class OrganizationSerializer4(serializers.ModelSerializer):
    org_logo = serializers.SerializerMethodField()
    org_images = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    def get_org_logo(self, obj):
        if obj.org_logo:
            return image_path_to_binary(obj.org_logo)
        return None
    def get_org_images(self, obj):
        if obj.org_images:
            return image_path_to_binary(obj.org_images)
        return None
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Fields to check for empty or null values
        fields_to_check = [
            'org_logo', 'org_images', 'organization_name', 'chairman', 
            'web_url', 'reg_id', 'org_detail', 'est_by', 'location','user','est_date','mission','organization_members'
           
        ]
        
        # Set a default value of "data not found" for empty or unwanted values
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null']:
                representation[field] = "data not found"
        
        return representation




 

class OrganizationSerializer6(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['_id','organization_name','org_logo','org_images']     



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo','organization_name']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation   



