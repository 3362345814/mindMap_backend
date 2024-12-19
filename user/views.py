from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, ResetPasswordSerializer, UpdateUsernameSerializer, \
    UpdateAPIKeyAndBaseURLSerializer
from .service.code_service import verify_code, send_verification_email

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if not verify_code(request.data.get("email"), request.data.get("code")):
            return Response({"error": "Invalid or expired verification code."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User create success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        try:
            send_verification_email(email)
            return Response({'message': 'Verification code sent successfully'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        login_type = request.data.get('login_type')  # 区分登录方式
        password = request.data.get('password')
        code = request.data.get('code')

        if login_type == 'password':
            # 密码登录
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        elif login_type == 'code':
            # 验证码登录
            if verify_code(email, code):  # 自定义函数来验证验证码
                user, created = User.objects.get_or_create(email=email)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid login type"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        user = request.user  # 从Token中获取的用户信息
        user_data = {
            'user_info':{
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'ai_info':{
                'api_key': user.api_key,
                'model_configuration_id': user.model_configuration_id,
                'custom_base_url': user.custom_base_url,
                'custom_model': user.custom_model,
                'model_selection_status': user.model_selection_status,
            }
        }
        return Response(user_data)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            code = serializer.validated_data.get("code")
            password = serializer.validated_data.get("password")
            # 验证邮箱验证码
            if not verify_code(email, code):
                return Response({"error": "Invalid or expired verification code"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # 获取用户并更新密码
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 修改用户名
class UpdateUsernameView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user  # 获取当前用户
        serializer = UpdateUsernameSerializer(data=request.data)
        if serializer.is_valid():
            new_username = serializer.validated_data.get('username')
            user.username = new_username
            user.save()
            return Response({"message": "Username updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAPIKeyAndBaseURLView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user  # 获取当前用户

        try:
            # 直接从请求数据中获取信息，而不进行序列化验证
            api_key = request.data.get('api_key', user.api_key)
            model_configuration_id = request.data.get('model_configuration_id', user.model_configuration_id)
            custom_model = request.data.get('custom_model', user.custom_model)
            custom_base_url = request.data.get('custom_base_url', user.custom_base_url)
            model_selection_status = request.data.get('model_selection_status', user.model_selection_status)

            # 更新用户信息
            user.api_key = api_key
            user.model_configuration_id = model_configuration_id
            user.custom_model = custom_model
            user.custom_base_url = custom_base_url
            user.model_selection_status = model_selection_status

            # 保存用户信息
            user.save()

            return Response({"message": "API Key and Base URL updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)