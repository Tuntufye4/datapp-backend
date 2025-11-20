from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Case
from .serializers import CaseSerializer

   
class CHWCaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    serializer_class = CaseSerializer   
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-district')
    def by_district(self, request):
        """
        Returns the number of cases per district filtered by patient_name if provided.
        """
        qs = Case.objects.all()
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('district')
            .annotate(count=Count('id'))
            .order_by('district')
        )
        return Response(list(data))

    @action(detail=False, methods=['get'], url_path='gender-distribution')
    def gender_distribution(self, request):

        """
        Returns the number of cases per gender filtered by patient_name if provided.
        """

        qs = Case.objects.all()
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('sex')
            .annotate(count=Count('id'))
            .order_by('sex')
        )
        return Response(list(data))  

    @action(detail=False, methods=['get'], url_path='disease-distribution')
    def disease_distribution(self, request):
        """
        Returns the number of cases per disease filtered by patient_name if provided.
        """
        qs = Case.objects.all()
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('disease')
            .annotate(count=Count('id'))
            .order_by('disease')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='visits')
    def visits(self, request):

        qs = Case.objects.all()
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('visit_type') 
            .annotate(count=Count('id'))
            .order_by('visit_type')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='house_type')
    def house_type(self, request):

        qs = Case.objects.all()
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('housing_type') 
            .annotate(count=Count('id'))
            .order_by('housing_type')
        )  
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='reporting_methods')  
    def reporting_methods(self, request):

        qs = Case.objects.all()  
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('reporting_method') 
            .annotate(count=Count('id'))
            .order_by('reporting_method')
        )  
        return Response(list(data))

    @action(detail=False, methods=['get'], url_path='treatments')  
    def treatments(self, request):

        qs = Case.objects.all()  
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('treatment') 
            .annotate(count=Count('id'))
            .order_by('treatment')
        )  
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='followupplan')  
    def followupplan(self, request):

        qs = Case.objects.all()  
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        data = (
            qs.values('follow_up_plan') 
            .annotate(count=Count('id'))  
            .order_by('follow_up_plan')
        )  
        return Response(list(data))
    

    @action(detail=False, methods=['get'], url_path='encounterlocation')  
    def encounterlocation(self, request):

        qs = Case.objects.all()  
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)     

        data = (
            qs.values('encounter_location') 
            .annotate(count=Count('id'))  
            .order_by('encounter_location')   
        )  
        return Response(list(data))
    

    @action(detail=False, methods=['get'], url_path='statistics')   
    def statistics(self, request):
        """
        Returns general statistics filtered by patient_name if provided.
        """
        qs = Case.objects.all()
        patient_name = request.query_params.get("patient_name")
        if patient_name:
            qs = qs.filter(patient_name__icontains=patient_name)

        total_cases = qs.count()
        male_cases = qs.filter(sex='Male').count()
        female_cases = qs.filter(sex='Female').count()
        confirmed_cases = qs.filter(classification='Confirmed').count()
        probable_cases = qs.filter(classification='Probable').count()   
        per_housing_type = qs.filter(housing_type='Permanent').count()
        sem_housing_type = qs.filter(housing_type='Semi-permanent').count()
        out_visit_type = qs.filter(visit_type='Outpatient').count()
        inp_visit_type = qs.filter(visit_type='Inpatient').count()
        em_visit_type = qs.filter(visit_type='Emergency').count()   


        # Calculate average cases per patient (using distinct patient_name)
        distinct_patients = qs.values("patient_name").distinct().count()
        avg_total_cases = total_cases / distinct_patients if distinct_patients > 0 else 0

        # Distinct male/female patients
        distinct_male_patients = qs.filter(sex="Male").values("patient_name").distinct().count()
        avg_male_cases = male_cases / distinct_male_patients if distinct_male_patients > 0 else 0

        distinct_female_patients = qs.filter(sex="Female").values("patient_name").distinct().count()
        avg_female_cases = female_cases / distinct_female_patients if distinct_female_patients > 0 else 0
        
      
   
        return Response({
            "total_cases": total_cases,  
            "male_cases": male_cases,
            "female_cases": female_cases, 
            "confirmed_cases": confirmed_cases, 
            "probale_cases": probable_cases,     
            "avg_total_cases": round(avg_total_cases, 2),   
            "avg_male_cases": round(avg_male_cases, 2),
            "avg_female_cases": round(avg_female_cases, 2),
            "per_housing_type": per_housing_type,  
            "sem_housing_type": sem_housing_type,
            "out_visit_type": out_visit_type,   
            "inp_visit_type": inp_visit_type,
            "em_visit_type": em_visit_type,
        })         

               