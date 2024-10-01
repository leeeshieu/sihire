from rest_framework import serializers
from users.models import User, Applicant, Director, GeneralAffairs, ProjectManager, Admin
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id",'email','username','name','phone','role','foto','is_active')

class ApplicantSerializer(serializers.ModelSerializer):
    user= UserSerializer()
    class Meta:
        model = Applicant
        fields = ("applicant_id", "user","application_list","is_accepted")
        
class ApplicantSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ("applicant_id", "user","application_list","is_accepted")

class DirectorSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Director
        fields = ("user",)

class DirectorSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("user",)

class GeneralAffairsSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = GeneralAffairs
        fields = ("user",)

class GeneralAffairsSerializer2(serializers.ModelSerializer):
    class Meta:
        model = GeneralAffairs
        fields = ("user",)

class ProjectManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProjectManager
        fields = ("user",)

class ProjectManagerSerializer2(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager
        fields = ("user",)

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Admin
        fields = ("user",)

class AdminSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ("user",)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'name', 'role', 'foto', 'phone')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        if role is not None:
            instance.role = role

        instance.save()
        return instance
