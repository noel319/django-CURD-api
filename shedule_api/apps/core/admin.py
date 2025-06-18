from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    
    def get_queryset(self, request):
        
        return self.model.all_objects.get_queryset()