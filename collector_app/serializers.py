from rest_framework import serializers

from collector_app.models import CollectorQuoter, Bar, BarCbrDay


class CollectorQuoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectorQuoter
        fields = '__all__'


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = '__all__'


class BarCbrDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BarCbrDay
        fields = '__all__'
