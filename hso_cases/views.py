from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Case
from .serializers import CaseSerializer   


class HSOCaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    serializer_class = CaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return cases created by the logged-in user
        return Case.objects.filter(created_by=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-district')
    def by_district(self, request):
        """
        Returns case counts by district for the logged-in user.
        """
        data = (
            self.get_queryset()
            .values('district')
            .annotate(count=Count('id'))
            .order_by('district')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'], url_path='disease-distribution')
    def disease_distribution(self, request):
        """
        Returns case counts by disease for the logged-in user.
        """
        data = (
            self.get_queryset()
            .values('disease')
            .annotate(count=Count('id'))
            .order_by('disease')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """
        Returns general statistics for the logged-in user.
        """
        total_cases = self.get_queryset().count()
        male_cases = self.get_queryset().filter(sex='Male').count()
        female_cases = self.get_queryset().filter(sex='Female').count()  
        

        return Response({
            "total_cases": total_cases,
            "male_cases": male_cases,
            "female_cases": female_cases   
        })
     