from django.shortcuts import render
import requests
from .models import Diseases
from .serializers import DiseasesSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create and Retrieve data.
base_url = 'https://rr-africa.oie.int/en/immediate-notifications-in-africa/'

@api_view(['GET', 'POST'])
def diseases_list(request):
    if request.method =='GET':
        all_diseases= Diseases.objects.all()
        serializer=DiseasesSerializers(all_diseases, many=True)
        return Response(serializer.data)
    elif request.method =='POST':
        serializer = DiseasesSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get, Update and delete particular disease details
@api_view(['GET','PUT','DELETE'])
def detail(requst, pk):
    # First let's check if the disease exist
    try:
        disease = Diseases.objects.get(pk=pk)

    except Diseases.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if requst.method =='GET':
        serializer = DiseasesSerializers(disease)
        return Response(serializer.data)

    elif requst.method =='PUT':
        serializer = DiseasesSerializers(instance=disease, data=requst.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif requst.method == 'DELETE':
        disease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







