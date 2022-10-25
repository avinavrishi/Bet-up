from rest_framework import serializers 
from accounts.models import Result
 
 
class ResultSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Result
        fields = ('Result_id',
                  'Red',
                  'Green',
                  'Blue',
                  'finalColor',
                  'user')