from rest_framework import serializers
from .models import Diseases


class DiseasesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diseases
        fields = '__all__'
