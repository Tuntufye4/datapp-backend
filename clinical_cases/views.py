from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Case
from .serializers import CaseSerializer

class ClinicalCaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    serializer_class = CaseSerializer    
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.patient_name)

    @action(detail=False, methods=['get'], url_path='by-district')
    def by_district(self, request):
        """
        Returns the number of cases per district for the logged-in user.
        """
        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('district')
            .annotate(count=Count('id'))
            .order_by('district')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'], url_path='disease-distribution')
    def disease_distribution(self, request):
        """
        Returns the number of cases per disease for the logged-in user.
        """
        data = (
            Case.objects
            .filter(created_by=request.patient_name)
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
        total_cases = Case.objects.filter(created_by=request.patient_name).count()
        male_cases = Case.objects.filter(created_by=request.patient_name, sex='Male').count()
        female_cases = Case.objects.filter(created_by=request.patient_name, sex='Female').count()
        classification_prob = Case.objects.filter(created_by=request.patient_name, classification='Probable').count()
        classification_conf = Case.objects.filter(created_by=request.patient_name, classification='Confirmed').count()
        total_admission_status = Case.objects.filter(created_by=request.patient_name).count()
        dis_admission_status = Case.objects.filter(created_by=request.patient_name, admission_status='Discharged').count()
        out_admission_status = Case.objects.filter(created_by=request.patient_name, admission_status='Outpatient').count()
        ref_admission_status = Case.objects.filter(created_by=request.patient_name, admission_status='Referred').count()


        return Response({
            "total_cases": total_cases,
            "male_cases": male_cases,
            "female_cases": female_cases,
            "classification_prob": classification_prob,
            "classification_conf": classification_conf,
            "total_admission_status": total_admission_status,
            "dis_admission_status": dis_admission_status,
            "out_admission_status": out_admission_status,
            "ref_admission_status": ref_admission_status,
        })  
    