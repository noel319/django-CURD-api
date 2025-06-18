from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from apps.core.models import BaseModel
from apps.core.managers import ActiveManager, AllObjectsManager


class Schedule(BaseModel):    
    name = models.CharField(max_length=255, help_text="Name of the schedule")
    description = models.TextField(blank=True, help_text="Description of the schedule")
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='schedules',
        help_text="Owner of the schedule"
    )

    objects = ActiveManager()
    all_objects = AllObjectsManager()

    class Meta:
        db_table = 'schedules'
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

    def get_schedule_data(self):        
        schedule_data = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []
        }

        for time_slot in self.time_slots.all():
            day_data = {
                'start': time_slot.start_time.strftime('%H:%M'),
                'stop': time_slot.end_time.strftime('%H:%M'),
                'ids': time_slot.ids
            }
            schedule_data[time_slot.day_of_week].append(day_data)

        return {'schedule': schedule_data}


class TimeSlot(BaseModel):    
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='time_slots',
        help_text="Schedule this time slot belongs to"
    )
    day_of_week = models.CharField(
        max_length=10,
        choices=DAYS_OF_WEEK,
        help_text="Day of the week"
    )
    start_time = models.TimeField(help_text="Start time of the slot")
    end_time = models.TimeField(help_text="End time of the slot")
    ids = models.JSONField(
        default=list,
        help_text="List of IDs associated with this time slot"
    )

    objects = ActiveManager()
    all_objects = AllObjectsManager()

    class Meta:
        db_table = 'time_slots'
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'
        ordering = ['day_of_week', 'start_time']
        unique_together = ['schedule', 'day_of_week', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.schedule.name} - {self.day_of_week} ({self.start_time}-{self.end_time})"

    def clean(self):        
        super().clean()
        
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
        
        if not isinstance(self.ids, list):
            raise ValidationError("IDs must be a list.")
        
        if not all(isinstance(id_val, int) and id_val > 0 for id_val in self.ids):
            raise ValidationError("All IDs must be positive integers.")

    def save(self, *args, **kwargs):        
        self.clean()
        super().save(*args, **kwargs)