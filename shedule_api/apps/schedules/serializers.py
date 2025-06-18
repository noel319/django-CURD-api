
from rest_framework import serializers
from .models import Schedule, TimeSlot



class TimeSlotSerializer(serializers.ModelSerializer):   
    start = serializers.TimeField(source='start_time', format='%H:%M')
    stop = serializers.TimeField(source='end_time', format='%H:%M')

    class Meta:
        model = TimeSlot
        fields = ['id', 'day_of_week', 'start', 'stop', 'ids']
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate_ids(self, value):

        if not isinstance(value, list):
            raise serializers.ValidationError("IDs must be a list.")
        
        if not value:
            raise serializers.ValidationError("IDs list cannot be empty.")
        
        for id_val in value:
            if not isinstance(id_val, int) or id_val <= 0:
                raise serializers.ValidationError("All IDs must be positive integers.")
        
        return value

    def validate(self, data):
       
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("Start time must be before end time.")
        
        return data


class ScheduleDataSerializer(serializers.Serializer):
   
    monday = TimeSlotSerializer(many=True, required=False)
    tuesday = TimeSlotSerializer(many=True, required=False)
    wednesday = TimeSlotSerializer(many=True, required=False)
    thursday = TimeSlotSerializer(many=True, required=False)
    friday = TimeSlotSerializer(many=True, required=False)
    saturday = TimeSlotSerializer(many=True, required=False)
    sunday = TimeSlotSerializer(many=True, required=False)


class ScheduleCreateUpdateSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    schedule = ScheduleDataSerializer()

    def validate_schedule(self, value):
        
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        for day in value.keys():
            if day not in valid_days:
                raise serializers.ValidationError(f"Invalid day: {day}")
        
        return value

    def create(self, validated_data):
        
        schedule_data = validated_data.pop('schedule')
        user = self.context['request'].user
        
        schedule = Schedule.objects.create(
            owner=user,
            **validated_data
        )
        
        self._create_time_slots(schedule, schedule_data)
        return schedule

    def update(self, instance, validated_data):
        
        schedule_data = validated_data.pop('schedule', None)
        
        # Update schedule fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if schedule_data:
            # Delete existing time slots
            instance.time_slots.all().delete()
            # Create new time slots
            self._create_time_slots(instance, schedule_data)
        
        return instance

    def _create_time_slots(self, schedule, schedule_data):
        
        time_slots_to_create = []
        
        for day, slots in schedule_data.items():
            for slot_data in slots:
                time_slot = TimeSlot(
                    schedule=schedule,
                    day_of_week=day,
                    start_time=slot_data['start_time'],
                    end_time=slot_data['end_time'],
                    ids=slot_data['ids']
                )
                time_slots_to_create.append(time_slot)
        
        TimeSlot.objects.bulk_create(time_slots_to_create)


class ScheduleListSerializer(serializers.ModelSerializer):
  
    owner = serializers.StringRelatedField(read_only=True)
    time_slots_count = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'owner', 'time_slots_count', 'created_at', 'updated_at']

    def get_time_slots_count(self, obj):
        
        return obj.time_slots.count()


class ScheduleDetailSerializer(serializers.ModelSerializer):
   
    owner = serializers.StringRelatedField(read_only=True)
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'owner', 'schedule', 'created_at', 'updated_at']

    def get_schedule(self, obj):
       
        schedule_data = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []
        }

        for time_slot in obj.time_slots.all():
            day_data = {
                'start': time_slot.start_time.strftime('%H:%M'),
                'stop': time_slot.end_time.strftime('%H:%M'),
                'ids': time_slot.ids
            }
            schedule_data[time_slot.day_of_week].append(day_data)

        return schedule_data