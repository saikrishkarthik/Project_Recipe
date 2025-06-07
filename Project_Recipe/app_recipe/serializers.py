from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
    
    
    def validate_name(self, value):   # name validation - name is unique and other fields are not blank
        if Recipe.objects.filter(name=value).exists():
            raise serializers.ValidationError("Recipe name must be unique.")
        return value

    def validate(self, data):  
        if self.partial:   # Check if this is a partial update (PATCH).
            return data         
        
        required_fields = ['name', 'description', 'ingredients', 'method', 'category']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} cannot be blank.")
        return data