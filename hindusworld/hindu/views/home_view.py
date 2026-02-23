# from rest_framework.views import APIView
# from rest_framework.response import Response
# from ..models.organization import Organization
# from ..models.event import Event
# from ..models.training import Training
# from ..serializers import OrganizationSerializer6, EventsSerializer3, TrainingSerializer4
# from ..utils import image_path_to_binary

# class HomeView(APIView):
#     def get(self, request):
#         # Retrieve the first 4 organizations globally
#         organizations = Organization.objects.all()[:4]
#         organization_serializer = OrganizationSerializer6(organizations, many=True)
        
#         # Convert organization images and logos to base64
#         for org in organization_serializer.data:
#             if 'org_images' in org and org['org_images']:
#                 org['org_images'] = image_path_to_binary(org['org_images'])
#             if 'org_logo' in org and org['org_logo']:
#                 org['org_logo'] = image_path_to_binary(org['org_logo'])

#         # Retrieve the first 4 events globally
#         events = Event.objects.all()[:4]
#         events_serializer = EventsSerializer3(events, many=True)

#         # Retrieve the first 4 trainings globally
#         trainings = Training.objects.all()[:4]
#         training_serializer = TrainingSerializer4(trainings, many=True)
        
#         # Convert training images to base64
#         for training in training_serializer.data:
#             if 'image' in training and training['image']:
#                 training['image'] = image_path_to_binary(training['image'])

#         return Response({
#             'organizations': organization_serializer.data,
#             'events': events_serializer.data,
#             'trainings': training_serializer.data,
#         })







from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.organization import Organization

from ..utils import image_path_to_binary
from ..models import EventCategory, TrainingCategory,Category,SubCategory
from ..serializers import EventCategorySerializer, TrainingCategorySerializer,SubCategorySerializer,CategorySerializer


class HomeView(APIView):
    def get(self, request):
        # Retrieve the first three organization categories
        categories = Category.objects.all()[:4]  # Fetch the first 3 Category objects
        categories_data = []

        if categories:
            # Serialize the categories if they exist
            category_serializer = CategorySerializer(categories, many=True)
            categories_data = category_serializer.data

        # Retrieve specific event categories by ID
        event_ids = [
            "a667b7f9-0a23-4bb6-bcd3-f042cb7a9060",
            "fe9c2beb-fdff-4658-9b7b-abf91d08e15d",
            "7426b52b-4046-4fe8-9d04-278a9d3562f8",
            "d8d437e8-1a6c-49ea-8cb6-55398bfd0989"
        ]
        event_categories = EventCategory.objects.filter(_id__in=event_ids)
        event_categories_data = EventCategorySerializer(event_categories, many=True).data

        # Retrieve the specified range of training categories
        training_categories = TrainingCategory.objects.all()[3:7]
        training_categories_data = TrainingCategorySerializer(training_categories, many=True).data

        # Retrieve the specific SubCategory by _id
        subcategory = SubCategory.objects.filter(_id="03b2952e-58ff-44e0-9960-f0ff5ab4ed05").first()
        subcategory_data = None

        if subcategory:
            # Serialize the SubCategory if it exists
            subcategory_serializer = SubCategorySerializer(subcategory)
            subcategory_data = subcategory_serializer.data

        # Return the response with all the data
        return Response({
            "organizationCategories": categories_data,
            "eventCategories": event_categories_data,
            "trainingCategories": training_categories_data 
        })