from django.contrib import admin
from .models import Schedule, TimeSlot


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'owner')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'owner')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'is_active'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'day_of_week', 'start_time', 'end_time', 'ids_display', 'is_active')
    list_filter = ('day_of_week', 'is_active', 'schedule')
    search_fields = ('schedule__name', 'schedule__owner__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    def ids_display(self, obj):
        return ', '.join(map(str, obj.ids[:5])) + ('...' if len(obj.ids) > 5 else '')
    ids_display.short_description = 'IDs'