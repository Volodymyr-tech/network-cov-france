from rest_framework import serializers
from app.models import MobileSite, Operator


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['code', 'name']


class MobileSiteSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer()

    class Meta:
        model = MobileSite
        fields = ['operator', 'city', 'has_2g', 'has_3g', 'has_4g']
