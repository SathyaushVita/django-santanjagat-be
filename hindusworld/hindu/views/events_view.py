# from rest_framework import viewsets,generics
# from ..models import Events
# from ..serializers import *
# from ..models import Organization, Country,Continent,Register,District,Events
# from rest_framework import status
# from rest_framework import status as http_status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from django.db.models import Q
# from django.core.mail import send_mail
# from django.conf import settings
# from datetime import datetime
# from ..utils import save_image_to_azure
# from django.utils import timezone
# from rest_framework.exceptions import ValidationError
# from ..enums import EventStatusEnum
# from rest_framework.exceptions import ValidationError
# from rest_framework import viewsets, pagination
# from rest_framework.exceptions import ValidationError
# from django.utils import timezone
# from django.db.models import Case, When, Value, IntegerField, ExpressionWrapper





# class CustomPagination(pagination.PageNumberPagination):
#     page_size = 100
#     page_size_query_param = 'page_size'
#     max_page_size = 100




# class EventsViewSet(viewsets.ModelViewSet):
#     queryset = Events.objects.all()
#     serializer_class = EventsSerializer1
#     # permission_classes = [IsAuthenticated]
#     # pagination_class = CustomPagination


#     def list(self, request):
#         # Extract query parameters for filtering
#         for event in Events.objects.all():
#             event.update_event_status()
#         filter_kwargs = request.query_params.dict()

#         # Add status filter to the query parameters
#         filter_kwargs['status'] = 'SUCCESS'

#         # Get the queryset filtered by the provided query parameters
#         queryset = Events.objects.filter(**filter_kwargs)

#         # If no results found
#         if not queryset.exists():
#             return Response({
#                 'message': 'Data not found',
#                 'status': 404
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Filter events based on their status
#         upcoming_events = queryset.filter(event_status="UPCOMING").order_by('start_date')
#         completed_events = queryset.filter(event_status="COMPLETED").order_by('start_date')

#         # Serialize both upcoming and completed events
#         event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
#         event_completed_serializer = self.get_serializer(completed_events, many=True)

#         # Return the formatted response
#         return Response({
#             "status": 200,
#             "event_upcoming": event_upcoming_serializer.data,
#             "event_completed": event_completed_serializer.data,
#         })


#     def retrieve(self, request, pk=None):
#         try:
#             instance = self.get_object()
#         except Events.DoesNotExist:
#             return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)





#     def create(self, request, *args, **kwargs):
#         try:
#             username = request.user.username
#             register_instance = Register.objects.get(username=username)
#             is_member = register_instance.is_member

#             if is_member == "false":
#                 return Response({
#                     "message": "Cannot create event. Membership details are required. Update your profile and become a member."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             created_at = timezone.now()

#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             instance = serializer.save()

#             # Process brochure
#             brochure = request.data.get('brochure')
#             if brochure and brochure != "null":
#                 saved_brochure_location = save_image_to_azure(brochure, instance._id, instance.name, 'eventbrochures')
#                 if saved_brochure_location:
#                     try:
#                         # Extract relative path from URL
#                         brochure_relative_path = saved_brochure_location.split('sathayushstorage.blob.core.windows.net/sathayush/')[1]
#                         instance.brochure = brochure_relative_path
#                     except IndexError:
#                         instance.brochure = saved_brochure_location  # Fallback to full URL if split fails
#                     instance.save()

#             # Process event images
#             event_images = request.data.get('event_images', [])
#             if event_images:
#                 saved_event_image_paths = []
#                 for image_data in event_images:
#                     if image_data and image_data != "null":
#                         saved_location = save_image_to_azure(image_data, instance._id, instance.name, 'hinduworld_events')
#                         if saved_location:
#                             try:
#                                 # Extract relative path from URL
#                                 event_image_relative_path = saved_location.split('sathayushstorage.blob.core.windows.net/sathayush/')[1]
#                                 saved_event_image_paths.append(event_image_relative_path)
#                             except IndexError:
#                                 saved_event_image_paths.append(saved_location)  # Fallback to full URL if split fails
#                 if saved_event_image_paths:
#                     instance.event_images = saved_event_image_paths
#                     instance.save()

#             # Send email notification
#             send_mail(
#                 'New Event Added',
#                 f'User ID: {request.user.id}\n'
#                 f'Contact Number: {register_instance.contact_number}\n'
#                 # f'Full Name: {request.user.get_full_name()}\n'
#                 f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
#                 f'Event ID: {instance._id}\n'
#                 f'Event Name: {instance.name}',
#                 settings.EMAIL_HOST_USER,
#                 [settings.EMAIL_HOST_USER],
#                 fail_silently=False,
#             )

#             # Return successful response with correct paths
#             return Response({
#                 "message": "Event added successfully.",
#                 "result": {
#                     **serializer.data,
#                     "brochure": instance.brochure,
#                     "event_images": instance.event_images
#                 }
#             }, status=status.HTTP_201_CREATED)

#         except Register.DoesNotExist:
#             return Response({
#                 "message": "User not found."
#             }, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({
#                 "message": "An error occurred.",
#                 "error": str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     def create(self, request, *args, **kwargs):
#         try:
#             username = request.user.username
#             register_instance = Register.objects.get(username=username)
#             is_member = register_instance.is_member

#             if is_member == "FALSE":
#                 return Response({
#                     "message": "Cannot create event. Membership details are required. Update your profile and become a member."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             created_at = timezone.now()

#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             brochure = request.data.get('brochure')
#             if brochure and brochure != "null":
#                 saved_brochure_location = save_image_to_azure(brochure, serializer.instance._id, serializer.instance.name, 'eventbrochures')
#                 if saved_brochure_location:
#                     serializer.instance.brochure = saved_brochure_location

#             event_images = request.data.get('event_images', [])
#             if event_images:
#                 saved_event_image_paths = []
#                 for image_data in event_images:
#                     if image_data and image_data != "null":
#                         saved_location = save_image_to_azure(image_data, serializer.instance._id, serializer.instance.name, 'hinduworldevents')
#                         if saved_location:
#                             saved_event_image_paths.append(saved_location)
#                 serializer.instance.event_images = saved_event_image_paths
#                 serializer.instance.save()

#             send_mail(
#                 'New Event Added',
#                 f'User ID: {request.user.id}\n'
#                 f'Contact Number: {register_instance.contact_number}\n'
#                 f'Full Name: {request.user.get_full_name()}\n'
#                 f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
#                 f'Event ID: {serializer.instance._id}\n'
#                 f'Event Name: {serializer.instance.name}',
#                 settings.EMAIL_HOST_USER,
#                 [settings.EMAIL_HOST_USER],
#                 fail_silently=False,
#             )

#             return Response({
#                 "message": "Event added successfully.",
#                 "result": serializer.data
#             }, status=status.HTTP_201_CREATED)

#         except Register.DoesNotExist:
#             return Response({
#                 "message": "User not found."
#             }, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({
#                 "message": "An error occurred.",
#                 "error": str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#     def update(self, request, pk=None):
#         try:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             updated_instance = serializer.save()
#             return Response({
#                 "message": "Updated successfully",
#                 "data": self.get_serializer(updated_instance).data
#             }, status=status.HTTP_200_OK)
#         except Events.DoesNotExist:
#             return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)







# class UpdateEventStatus(generics.GenericAPIView):
#     serializer_class = EventSerializer2

#     def put(self, request, event_id):
#         try:
#             event = Events.objects.get(pk=event_id, status='PENDING')
#         except Events.DoesNotExist:
#             return Response({
#                 'message': 'Event with PENDING status not found for the provided ID'
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Update the status to 'SUCCESS'
#         event.status = 'SUCCESS'
#         event.save()

#         # Serialize the updated event
#         serializer = self.get_serializer(event)

#         return Response({
#             'message': 'success',
#             'result': serializer.data
#         }, status=status.HTTP_200_OK)








 





# class GetEventsByLocation(generics.ListAPIView):
#     serializer_class = EventsSerializer1
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         input_value = self.request.query_params.get('input_value')
#         category = self.request.query_params.get('category')

#         # Validate that at least one of the filters is provided
#         if not input_value and not category:
#             raise ValidationError("At least one of 'input_value', 'category' is required.")

#         today = timezone.now().date()

#         # Define queries for each location level
#         if input_value:
#             # Try matching continent
#             continent_match = Events.objects.filter(object_id__state__country__continent__pk=input_value)
#             if continent_match.exists():
#                 queryset = continent_match
#             else:
#                 # Try matching country
#                 country_match = Events.objects.filter(object_id__state__country__pk=input_value)
#                 if country_match.exists():
#                     queryset = country_match
#                 else:
#                     # Try matching state
#                     state_match = Events.objects.filter(object_id__state__pk=input_value)
#                     if state_match.exists():
#                         queryset = state_match
#                     else:
#                         # Try matching district
#                         district_match = Events.objects.filter(object_id__pk=input_value)
#                         if district_match.exists():
#                             queryset = district_match
#                         else:
#                             # No match found, return an empty queryset
#                             queryset = Events.objects.none()
#         else:
#             queryset = Events.objects.all()

#         # Apply status filter to get only SUCCESS events
#         queryset = queryset.filter(status='SUCCESS')

#         # Apply category filtering
#         if category:
#             queryset = queryset.filter(category_id=category)

#         # Order by proximity to today's date
#         queryset = queryset.order_by(
#             Case(
#                 When(start_date__gte=today, then=Value(0)),  # Upcoming or today
#                 When(start_date__lt=today, then=Value(1)),   # Past events
#                 default=Value(2),
#                 output_field=IntegerField()
#             ),
#             'start_date'
#         )

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()

#         # Filter for upcoming and completed events
#         today = timezone.now().date()
#         upcoming_events = queryset.filter(start_date__gte=today)
#         completed_events = queryset.filter(start_date__lt=today)

#         # Paginate the upcoming events
#         page = self.paginate_queryset(upcoming_events)
#         if page is not None:
#             event_upcoming_serializer = self.get_serializer(page, many=True)
#             event_completed_serializer = self.get_serializer(completed_events, many=True)

#             return Response({
#                 "status": 200,
#                 "event_upcoming": event_upcoming_serializer.data,
#                 "event_completed": event_completed_serializer.data,
#             })

#         # If no pagination, return all events
#         event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
#         event_completed_serializer = self.get_serializer(completed_events, many=True)

#         return Response({
#             "status": 200,
#             "event_upcoming": event_upcoming_serializer.data,
#             "event_completed": event_completed_serializer.data,
#         })











































from ..serializers import *
from ..models import *
from rest_framework import viewsets
from rest_framework .response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from ..utils import CustomPagination, save_image_to_azure
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from ..enums import EventStatusEnum
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404



class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()
    def create(self, request, *args, **kwargs):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)
            # Attempt to find the Register instance by either email or contact number
            register_instance = None
            if email:
                register_instance = Register.objects.filter(email=email).first()
            elif contact_number:
                register_instance = Register.objects.filter(contact_number=contact_number).first()
            # If no user found, return error
            if not register_instance:
                return Response({
                    "message": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)
            # Check membership status
            is_member = register_instance.is_member
            if is_member == "false":
                return Response({
                    "message": "Cannot add Event. Membership details are required. Update your profile and become a member to add Temple."
                }, status=status.HTTP_400_BAD_REQUEST)
            # Extract image_location from request data
            image_locations = request.data.get('image_location', [])
            # If image_location is not a list, convert it to a list
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            # Add the image_location back to the request data, set it to "null" initially
            request.data['image_location'] = "null"
            # Serialize data and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            saved_locations = []  # To store valid saved locations
            # Check if image locations exist and are not null
            if image_locations and "null" not in image_locations:
                entity_type = "events"
                # Process each image location
                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)  # Add saved location to the list
            # If there are saved locations, update the instance's image_location field
            if saved_locations:
                serializer.instance.image_location = saved_locations  # Save as a list
                serializer.instance.save()
            # Capture the current time
            created_at = timezone.now()
            # Send email to EMAIL_HOST_USER
            send_mail(
                'New Event Added',
                f'User ID: {request.user.id}\n'
                # f'Full Name: {request.user.get_full_name()}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Temple ID: {serializer.instance._id}\n'
                f'Temple Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def list(self, request):
        # Initialize filter dictionary if you want to allow for future filtering logic
        filter_kwargs = {}
        # Filter the queryset based on any provided query parameters
        for key, value in request.query_params.items():
            filter_kwargs[key] = value
        queryset = Event.objects.filter(status='ACTIVE',**filter_kwargs)
        if not queryset.exists():
            return Response({
                'message': 'Data not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)
        # Filter events based on their status
        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        # Serialize the filtered events
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)
        if not filter_kwargs:
             return Response({
                "status": 200,
                "event_upcoming": event_upcoming_serializer.data,
                "event_completed": event_completed_serializer.data,
            })
        # Return the formatted response
        serializer = EventSerializer1(queryset, many=True)
        print("wdefrgnh")
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
        except Event.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer1(instance)
        return Response(serializer.data)
    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = EventSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        return Response({
            "message": "updated successfully",
            "data": EventSerializer1(updated_instance).data
        }, status=status.HTTP_200_OK)














class EventPost(generics.CreateAPIView):
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def post(self, request, *args, **kwargs):
        try:
            # Fetch the Register instance for the logged-in user using the username
            username = request.user.username  # Example: Using username
            print(f"Username: {username}")
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member
            print(f"is_member: {is_member}")

            # Check if the user is a member
            if is_member == "NO":
                print("User is not a member")
                return Response({
                    "message": "Cannot add the temple. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Register.DoesNotExist:
            return Response({
                "message": "User not found in Register."
            }, status=status.HTTP_404_NOT_FOUND)

        # Extract image_location from request data
        image_location = request.data.get('image_location')

        # Add the image_location back to the request data
        request.data['image_location'] = "null"

        # Serialize data and save
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if image_location and image_location != "null":
            saved_location = save_image_to_folder(image_location, serializer.instance._id, serializer.instance.name)
            print(saved_location, "=================================")
            if saved_location:
                serializer.instance.image_location = saved_location
                serializer.instance.save()

        return Response({
            "message": "success",
            "result": serializer.data
        })


# class GetEventsByLocation(generics.ListAPIView):
#     serializer_class = EventSerializer1
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         input_value = self.request.query_params.get('input_value')
#         category = self.request.query_params.get('category')

#         if not input_value and not category:
#             raise ValidationError("Input value or category is required")

#         # Define queries for each level
#         country_query = Q(object_id__block__district__state__country=input_value)
#         state_query = Q(object_id__block__district__state=input_value)
#         district_query = Q(object_id__block__district=input_value)
#         block_query = Q(object_id__block=input_value)
#         village_query = Q(object_id=input_value)

#         # Combine queries with OR operator
#         combined_query = Q()
#         if input_value:
#             combined_query |= country_query | state_query | district_query | block_query | village_query

#         # Apply category filter if provided
#         if category:
#             combined_query &= Q(category=category)

#         queryset = Event.objects.filter(combined_query).select_related(
#             'object_id__block__district__state__country',
#             'object_id__block__district__state',
#             'object_id__block__district',
#             'object_id__block',
#             'object_id'
#         )

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

class GetEventsByLocation(generics.ListAPIView):
    serializer_class = EventSerializer1
    pagination_class = CustomPagination
    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        if not input_value and not category:
            raise ValidationError("At least one of input_value or category must be provided.")
        today = timezone.now().date()
        # Define queries for each location level
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)
        # Combine location queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query
        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)
        # Filter by proximity to today's date and order by start date
        queryset = Event.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id'
        ).order_by(
            Case(
                When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                When(start_date__lt=today, then=Value(1)),   # Past events
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'
        )
        # Check if queryset is empty and filter directly by object_id
        if not queryset.exists() and input_value:
            queryset = Event.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)
            # Reorder by proximity to today's date and start date
            queryset = queryset.order_by(
                Case(
                    When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                    When(start_date__lt=today, then=Value(1)),   # Past events
                    default=Value(2),
                    output_field=IntegerField()
                ),
                'start_date'
            )
        return queryset
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        queryset = self.get_queryset().filter(status='ACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Filter for upcoming and completed events
            upcoming_events = queryset.filter(event_status="UPCOMING")
            completed_events = queryset.filter(event_status="COMPLETED")
            event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
            event_completed_serializer = self.get_serializer(completed_events, many=True)
            return Response({
                "status": 200,
                "event_upcoming": event_upcoming_serializer.data,
                "event_completed": event_completed_serializer.data,
            })
        serializer = self.get_serializer(queryset, many=True)
        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)
        return Response({
            "status": 200,
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
        })



class GetIndianEvents(APIView):
    def get(self, request):
        indian_location = Village.objects.all()
        event_query_set = Event.objects.all()
        indian_Events = event_query_set.filter(object_id__in=indian_location)
       


        paginator = PageNumberPagination()
        paginator.page_size = 50 
        indian_events_page = paginator.paginate_queryset(indian_Events, request)


        indianevents = EventSerializer1(indian_events_page, many=True)
        
        return paginator.get_paginated_response( indianevents.data)
        


class GetGlobalEvents(APIView):
    def get(self, request):
        Event_query_set = Event.objects.all()
        global_events = Event_query_set.exclude(geo_site__in=['S', 'D', 'B', 'V'])

        paginator = PageNumberPagination()
        paginator.page_size = 50 
        global_temples_page = paginator.paginate_queryset(global_events, request)

        globalevents = EventSerializer1(global_temples_page, many=True)

        return paginator.get_paginated_response( globalevents.data)


class GetbyStateLocationEvents(generics.ListAPIView):
    serializer_class = EventSerializer1

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        temples_in_state = Event.objects.filter(object_id__block__district__state_id=state_id)
        return temples_in_state
    
class GetbyDistrictLocationEvents(generics.ListAPIView):
    serializer_class = EventSerializer1

    def get_queryset(self):
        district_id =self.kwargs.get('district_id')
        temples_in_district = Event.objects.filter(object_id__block__district_id=district_id)
        return temples_in_district
    

   
class GetbyBlockLocationEvents(generics.ListAPIView):
    serializer_class = EventSerializer1

    def get_queryset(self):
        block_id = self.kwargs.get('block_id')
        temples_in_district = Event.objects.filter(object_id__block_id=block_id)
        return temples_in_district
    










class EventstatusView(generics.ListAPIView):
    serializer_class = EventSerializer1
    pagination_class = CustomPagination

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        now = timezone.now()

        queryset = Event.objects.all()

        # Update event statuses before returning the queryset
        for event in queryset:
            event.update_event_status()

        if status_param:
            if status_param not in dict(EventStatusEnum.__members__).keys():
                raise ValidationError("Invalid status value")
            queryset = queryset.filter(event_status=status_param)

        # Order events: upcoming events first, then completed events
        return queryset.order_by(
            Case(
                When(event_status=EventStatusEnum.UPCOMING.name, then=Value(0)),
                When(event_status=EventStatusEnum.COMPLETED.name, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'  # Further order by start date within each status group
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)