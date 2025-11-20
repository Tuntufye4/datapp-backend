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

    
    @action(detail=False, methods=['get'], url_path='case-source')
    def case_sources(self, request):  
        """
        Returns case counts by case_source for the logged-in user.
        """
        data = (
            self.get_queryset()
            .values('case_source')   
            .annotate(count=Count('id'))
            .order_by('case_source')   
        )
        return Response(list(data))


    @action(detail=False, methods=['get'], url_path='by-supervising-facility')
    def supervising_facility(self, request):
        """
        Returns case counts by supervising facility for the logged-in user.
        """    
        data = (
            self.get_queryset()
            .values('supervising_facility')      
            .annotate(count=Count('id'))
            .order_by('supervising_facility')   
        )
        return Response(list(data))

    
    @action(detail=False, methods=['get'], url_path='reporting_methods')
    def reporting_methods(self, request):
        """
        Returns case counts by disease for the logged-in user.
        """
        data = (
            self.get_queryset()
            .values('reporting_method')
            .annotate(count=Count('id'))
            .order_by('reporting_method')   
        )
        return Response(list(data))
    
    
    @action(detail=False, methods=['get'], url_path='treatment-distribution')
    def treatment_distribution(self, request):
        """
        Returns case counts by treatment type   
        """
        data = (
            self.get_queryset()
            .values('treatment')
            .annotate(count=Count('id'))
            .order_by('treatment')       
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='diagnosis-distribution')
    def diagnosis_distribution(self, request):
        """
        Returns case counts by diagnosis type.
        """
        data = (
            self.get_queryset()
            .values('diagnosis')
            .annotate(count=Count('id'))
            .order_by('diagnosis')       
        )
        return Response(list(data))
    
    
    @action(detail=False, methods=['get'], url_path='symptoms-distribution')
    def symptoms_distribution(self, request):
        """
        Returns case counts by symptoms.
        """
        data = (
            self.get_queryset()
            .values('symptoms')
            .annotate(count=Count('id'))
            .order_by('symptoms')       
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='vector_control')
    def vector_control(self, request):
        """
        Returns case counts by vector_control_measure.
        """
        data = (
            self.get_queryset()
            .values('vector_control_measure')
            .annotate(count=Count('id'))
            .order_by('vector_control_measure')       
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='env_risk_factors')
    def env_risk_factors(self, request):
        """
        Returns case counts by environmental risk factors.
        """
        data = (
            self.get_queryset()
            .values('environmental_risk_factors')
            .annotate(count=Count('id'))
            .order_by('environmental_risk_factors')       
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
        classification_prob = self.get_queryset().filter(Classification='Probable').count()
        classification_conf = self.get_queryset().filter(Classification='Confirmed').count()   
        sch_case_source =self.get_queryset().filter(case_source='School').count()
        bor_case_source = self.get_queryset().filter(case_source='Border_post').count()
        com_case_source = self.get_queryset().filter(case_source='Community').count()
        sms_reporting_method = self.get_queryset().filter(reporting_method='SMS').count()
        ele_reporting_method = self.get_queryset().filter(reporting_method='Electronic_form').count()
        sta_env_risk_factors = self.get_queryset().filter(environmental_risk_factors='Stagnant Water').count()
        pwd_env_risk_factors = self.get_queryset().filter(environmental_risk_factors='Poor Waste Disposal').count()
        bdr_env_risk_factors = self.get_queryset().filter(environmental_risk_factors='Blocked Drainage').count()

        return Response({
            "total_cases": total_cases,   
            "male_cases": male_cases,
            "female_cases": female_cases,  
            "classification_prob": classification_prob,  
            "classification_conf": classification_conf, 
            "sch_case_source" : sch_case_source,
            "bor_case_source" : bor_case_source,
            "com_case_source" : com_case_source,   
            "sms_reporting_method" : sms_reporting_method,
            "ele_reporting_method" : ele_reporting_method,   
            "sta_env_risk_factors": sta_env_risk_factors,
            "pwd_env_risk_factors": pwd_env_risk_factors,
            "bdr_env_risk_factors": bdr_env_risk_factors,
        })
        

        