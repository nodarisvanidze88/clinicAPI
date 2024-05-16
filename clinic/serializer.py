from rest_framework import serializers
from .models import CustomUser, Appointment,Doctor, Availability
from django.utils import timezone
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'status', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    
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
        queryset=CustomUser.objects.filter(status='patient'),
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
    
    def validate(self, data):
        scheduled_time = data.get('scheduled_time')
        treatment_duration = data.get('treatment_duration')
        doctor = data.get('doctor')
        
        if not scheduled_time or not treatment_duration or not doctor:
            raise serializers.ValidationError("Scheduled time, treatment duration, and doctor must be provided")

        end_time = scheduled_time + timezone.timedelta(minutes=treatment_duration)
        
        overlapping_appointments = Appointment.objects.filter(
            doctor=doctor,
            scheduled_time__lt=end_time,
            scheduled_time__gte=scheduled_time
        )
        
        if overlapping_appointments.exists():
            raise serializers.ValidationError("The doctor is not available at the scheduled time")

        availabilities = Availability.objects.filter(doctor=doctor)
        for availability in availabilities:
            if availability.start_time <= scheduled_time and availability.end_time >= end_time:
                return data
        
        raise serializers.ValidationError("The doctor's availability does not cover the entire appointment duration")

    
class AvailabilitySerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset = Doctor.objects.all(),
        write_only = True,
        source = 'doctor'
    )
    class Meta:
        model = Availability
        fields = '__all__'