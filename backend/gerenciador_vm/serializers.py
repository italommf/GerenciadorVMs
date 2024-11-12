from rest_framework import serializers
from .models import Maquinas_Virtuais

class MaquinasVirtuaisSerializer(serializers.ModelSerializer):

    class Meta:

        model = Maquinas_Virtuais
        fields = '__all__'

