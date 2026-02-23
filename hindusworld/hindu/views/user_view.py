# from ..serializers import UserSerializer,LoginSerializer,VerifySerializer,ResetSerializer,ResetSerializer,ResendOtpSerializer,RegisterSerializerl,VerifyOtpSerializer
from ..serializers import Register_LoginSerializer,Verify_LoginSerializer,MemberSerializer,MemberPicSerializer
from rest_framework import viewsets,generics
from ..models import Register
from rest_framework .views import APIView,status
from rest_framework .response import Response
from ..enums.user_status_enum import UserStatus
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import validate_email,send_email,send_sms,generate_otp,Resend_sms,send_welcome_email,image_path_to_binary,save_video_to_azure,video_path_to_binary
from django.contrib.auth import authenticate
from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..utils import save_image_to_azure
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from ..enums import MemberStatus



     

     
class Register_LoginView(generics.GenericAPIView):
    serializer_class = Register_LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        
        if not username:
            return Response({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        message = ""
        
        # Determine if username is an email or phone number
        if validate_email(username):
            # Check if user exists by email or contact number in gramadevata_updated
            user = Register.objects.using('gramadevata_updated1').filter(email=username).first() or \
                   Register.objects.using('gramadevata_updated1').filter(contact_number=username).first()
        else:
            # Check if user exists by contact number or email in gramadevata_updated
            user = Register.objects.using('gramadevata_updated1').filter(contact_number=username).first() or \
                   Register.objects.using('gramadevata_updated1').filter(email=username).first()
        if user:
            # Username already exists, update OTP
            user.verification_otp = otp
            user.verification_otp_created_time = timezone.now()
            user.save(using='gramadevata_updated1')
            message = "OTP sent successfully"
        else:
            # Username does not exist, create a new user with either email or contact number
            user = Register.objects.using('gramadevata_updated1').create(
                username=username,
                verification_otp=otp,
                verification_otp_created_time=timezone.now(),
                email=username if validate_email(username) else None,
                contact_number=username if not validate_email(username) else None
            )
            message = "OTP sent successfully"
        # Determine if username is an email or phone number
        if validate_email(username):
            send_email(username, otp)
        else:
            send_sms(username, otp)

        return Response({"otp": message}, status=status.HTTP_200_OK)





class Validate_LoginOTPView(generics.GenericAPIView):
    serializer_class = Verify_LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        verification_otp = request.data.get('verification_otp')
        
        user = None
        if validate_email(username):
            user = Register.objects.using('gramadevata_updated1').filter(email=username, verification_otp=verification_otp).first() or \
                   Register.objects.using('gramadevata_updated1').filter(contact_number=username, verification_otp=verification_otp).first()
        else:
            user = Register.objects.using('gramadevata_updated1').filter(contact_number=username, verification_otp=verification_otp).first() or \
                   Register.objects.using('gramadevata_updated1').filter(email=username, verification_otp=verification_otp).first()

        if user:
            # Check OTP expiration
            if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update user status to ACTIVE
        user.status = 'ACTIVE'
        user.save(using='gramadevata_updated1')

        # Send a welcome email if the username is an email
        if validate_email(username):
            send_welcome_email(username)
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'username': user.get_username(),
            'user_id': user.id,
            'is_member': user.is_member,  
            'profile_pic': user.profile_pic
        }, status=status.HTTP_200_OK)








class MemberDetailsViews(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = MemberPicSerializer
    permission_classes = [IsAuthenticated]


class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Register.objects.all()
        response_data = []
        for item in queryset:
            item_data = MemberSerializer(item).data

            # Process profile_pic
            profile_pic_path = item.profile_pic
            if profile_pic_path:
                encoded_string = image_path_to_binary(profile_pic_path)
                item_data['profile_pic'] = encoded_string.decode('utf-8') if encoded_string else None
            else:
                item_data['profile_pic'] = None

            # Process certificate
            certificate_path = item.certificate
            if certificate_path:
                encoded_string = image_path_to_binary(certificate_path)
                item_data['certificate'] = encoded_string.decode('utf-8') if encoded_string else None
            else:
                item_data['certificate'] = None

            response_data.append(item_data)

        return Response(response_data, status=status.HTTP_200_OK)






class GetProfileById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        item = get_object_or_404(Register, id=id)
        item_data = MemberSerializer(item).data

        # Process profile_pic
        profile_pic_path = item.profile_pic
        if profile_pic_path:
            encoded_string = image_path_to_binary(profile_pic_path)
            item_data['profile_pic'] = encoded_string if encoded_string else None
        else:
            item_data['profile_pic'] = None

        # Process certificate
        certificate_path = item.certificate
        if certificate_path:
            encoded_string = image_path_to_binary(certificate_path)
            item_data['certificate'] = encoded_string if encoded_string else None
        else:
            item_data['certificate'] = None

        return Response(item_data, status=status.HTTP_200_OK)








class UpdateMemberDetails(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def put(self, request, id):
            instance = get_object_or_404(Register, id=id)
            profile_pic = request.data.get('profile_pic')
            certificate = request.data.get('certificate')

            # Clone request data to allow modification
            mutable_data = request.data.copy()

            # Check if email or contact_number is being updated
            new_email = mutable_data.get('email', instance.email)
            new_contact_number = mutable_data.get('contact_number', instance.contact_number)

            # Check if the new email is already in use by another user
            if new_email != instance.email:
                if Register.objects.filter(email=new_email).exclude(id=instance.id).exists():
                    return Response({"error": "Email already in use by another account"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new contact number is already in use by another user
            if new_contact_number != instance.contact_number:
                if Register.objects.filter(contact_number=new_contact_number).exclude(id=instance.id).exists():
                    return Response({"error": "Contact number already in use by another account"}, status=status.HTTP_400_BAD_REQUEST)

            # Proceed with the update if email and contact_number are unique
            serializer = self.get_serializer(instance, data=mutable_data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['is_member'] = MemberStatus.true.value
            serializer.save()

            # Profile Pic handling
            if profile_pic and profile_pic != "null":
                saved_location = save_image_to_azure(profile_pic, serializer.instance.id, serializer.instance.full_name, 'profile_pic')
                if saved_location:
                    serializer.instance.profile_pic = saved_location
            else:
                serializer.instance.profile_pic = None

            # Certificate handling
            if certificate and certificate != "null":
                saved_location = save_image_to_azure(certificate, serializer.instance.id, serializer.instance.full_name, 'certificate')
                if saved_location:
                    serializer.instance.certificate = saved_location
            else:
                serializer.instance.certificate = None

            serializer.instance.save()

            # Update response data
            response_data = MemberSerializer(serializer.instance).data
            if not profile_pic or profile_pic == "null":
                response_data['profile_pic'] = None
            if not certificate or certificate == "null":
                response_data['certificate'] = None
            
            return Response(response_data, status=status.HTTP_200_OK)