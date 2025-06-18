from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Schedule, TimeSlot
from .serializers import (
    ScheduleListSerializer,
    ScheduleDetailSerializer,
    ScheduleCreateUpdateSerializer,
)


class ScheduleListCreateAPIView(generics.ListCreateAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        return Schedule.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        
        if self.request.method == 'POST':
            return ScheduleCreateUpdateSerializer
        return ScheduleListSerializer

    @swagger_auto_schema(
        operation_description="Get list of schedules for the authenticated user",
        responses={
            200: ScheduleListSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new schedule",
        request_body=ScheduleCreateUpdateSerializer,
        responses={
            201: ScheduleDetailSerializer,
            400: "Bad Request",
            401: "Unauthorized"
        }
    )
    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()
        
        detail_serializer = ScheduleDetailSerializer(schedule)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ScheduleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        
        return Schedule.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        
        if self.request.method in ['PUT', 'PATCH']:
            return ScheduleCreateUpdateSerializer
        return ScheduleDetailSerializer

    @swagger_auto_schema(
        operation_description="Get a specific schedule",
        responses={
            200: ScheduleDetailSerializer,
            401: "Unauthorized",
            404: "Not Found"
        }
    )
    def get(self, request, *args, **kwargs):
        
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific schedule",
        request_body=ScheduleCreateUpdateSerializer,
        responses={
            200: ScheduleDetailSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found"
        }
    )
    def put(self, request, *args, **kwargs):
        
        return self._update_schedule(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific schedule",
        request_body=ScheduleCreateUpdateSerializer,
        responses={
            200: ScheduleDetailSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found"
        }
    )
    def patch(self, request, *args, **kwargs):
        
        return self._update_schedule(request, *args, **kwargs)

    def _update_schedule(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()        
        
        detail_serializer = ScheduleDetailSerializer(schedule)
        return Response(detail_serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a specific schedule",
        responses={
            204: "No Content",
            401: "Unauthorized",
            404: "Not Found"
        }
    )
    def delete(self, request, *args, **kwargs):
        
        return super().delete(request, *args, **kwargs)


@swagger_auto_schema(
    method='get',
    operation_description="Get a protected endpoint that requires JWT authentication",
    responses={
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_STRING),
                    'schedules_count': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        ),
        401: "Unauthorized"
    },
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="JWT token in format: Bearer <token>",
            type=openapi.TYPE_STRING,
            required=True
        )
    ]
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def protected_endpoint(request):
    
    user = request.user
    schedules_count = Schedule.objects.filter(owner=user).count()
    
    return Response({
        'message': f'Hello {user.username}! This is a protected endpoint.',
        'user': user.username,
        'user_id': user.id,
        'schedules_count': schedules_count,
        'is_staff': user.is_staff,
        'date_joined': user.date_joined.isoformat(),
    })


@swagger_auto_schema(
    method='get',
    operation_description="Get schedule statistics for the authenticated user",
    responses={
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_schedules': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'total_time_slots': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'schedules_by_day': openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )
        ),
        401: "Unauthorized"
    }
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def schedule_statistics(request):
    
    user = request.user
    schedules = Schedule.objects.filter(owner=user)
    total_schedules = schedules.count()
    
    total_time_slots = TimeSlot.objects.filter(schedule__owner=user).count()    
    
    schedules_by_day = {}
    for day, _ in TimeSlot.DAYS_OF_WEEK:
        count = TimeSlot.objects.filter(
            schedule__owner=user, 
            day_of_week=day
        ).count()
        schedules_by_day[day] = count
    
    return Response({
        'total_schedules': total_schedules,
        'total_time_slots': total_time_slots,
        'schedules_by_day': schedules_by_day,
        'user': user.username,
    })