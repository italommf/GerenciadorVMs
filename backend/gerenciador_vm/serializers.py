from rest_framework import serializers
from .models import Maquinas_Virtuais, Robotizacoes

class MaquinasVirtuaisSerializer(serializers.ModelSerializer):

    class Meta:

        model = Maquinas_Virtuais
        fields = '__all__'

class RobotizacoesSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Robotizacoes
        fields = '__all__'
