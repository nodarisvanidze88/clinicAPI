from rest_framework import serializers
from .models import CustomUser, Appointment,Doctor, Availability

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'status', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = CustomUser.objects.all(),
        write_only = True,
        source = 'user'
    )
    class Meta:
        model = Doctor
        fields = "__all__"
    
class AppointmentSerializer(serializers.ModelSerializer):
    patient = CustomUserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True,
        source='patient'
    )
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True,
        source='doctor'
    )

    class Meta:
        model = Appointment
        fields = '__all__'
    
class AvailabilitySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset = Doctor.objects.all(),
        write_only = True
    )
    class Meta:
        model = Availability
        fields = '__all__'