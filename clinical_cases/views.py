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


    @action(detail=False, methods=['get'], url_path='gender-distribution')
    def gender_distribution(self, request):
        """
        Returns the number of cases per for the logged-in user.
        """
        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('sex')
            .annotate(count=Count('id'))
            .order_by('sex')
        )
        return Response(list(data))


    @action(detail=False, methods=['get'], url_path='diagnosis-distribution')
    def diagnosis_distribution(self, request):
        """
        Returns the number of cases per diagnosis type for the logged-in user.
        """
        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('diagnosis')
            .annotate(count=Count('id'))
            .order_by('diagnosis')
        )
        return Response(list(data))


    
    @action(detail=False, methods=['get'], url_path='treatment-distribution')
    def treatment_distribution(self, request):
        """
        Returns the number of cases per treatment type for the logged-in user.
        """
        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('treatment')
            .annotate(count=Count('id'))
            .order_by('treatment')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'], url_path='symptoms-distribution')
    def symptoms_distribution(self, request):
        """
        Returns the number of cases per symptoms for the logged-in user.
        """
        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('symptoms')
            .annotate(count=Count('id'))
            .order_by('symptoms')
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
    

    @action(detail=False, methods=['get'], url_path='house_types')
    def house_types(self, request):

        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('housing_type')
            .annotate(count=Count('id'))
            .order_by('housing_type')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='classifications')
    def classifications(self, request):

        data = (
            Case.objects
            .filter(created_by=request.patient_name)
            .values('classification')
            .annotate(count=Count('id'))   
            .order_by('classification')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='admission-stats')
    def admissionstats(self, request):

        data = (

            Case.objects
            .filter(created_by=request.patient_name)
            .values('admission_status')
            .annotate(count=Count('id'))
            .order_by('admission_status')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='vitals')
    def vitals(self, request):

        data = (

            Case.objects
            .filter(created_by=request.patient_name)
            .values('vital_signs')
            .annotate(count=Count('id'))
            .order_by('vital_signs')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='triage')
    def triage(self, request):

        data = (

            Case.objects
            .filter(created_by=request.patient_name)
            .values('triage_level')
            .annotate(count=Count('id'))
            .order_by('triage_level')
        )
        return Response(list(data))
    

    @action(detail=False, methods=['get'], url_path='procedures-done')
    def proceduresdone(self, request):

        data = (    
            Case.objects
            .filter(created_by=request.patient_name)
            .values('procedures_done')    
            .annotate(count=Count('id'))
            .order_by('procedures_done')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='lab-tests-ordered')
    def labtestsordered(self, request):  

        data = (    
            Case.objects
            .filter(created_by=request.patient_name)
            .values('lab_tests_ordered')    
            .annotate(count=Count('id'))
            .order_by('lab_tests_ordered')
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
        tem_vitals = Case.objects.filter(created_by=request.patient_name, vital_signs='Temperature').count()
        pulse_vitals = Case.objects.filter(created_by=request.patient_name, vital_signs='Pulse').count()
        respiratory_vitals = Case.objects.filter(created_by=request.patient_name, vital_signs='Respiratory Rate').count()

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
            "tem_vitals": tem_vitals,
            "pulse_vitals":pulse_vitals,  
            "respiratory_vitals": respiratory_vitals,
        })  
    