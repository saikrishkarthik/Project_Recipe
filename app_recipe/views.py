import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Recipe
from user_auth.views import TokenAuthentication
from .serializers import RecipeSerializer
from django.db.models import Q
from rest_framework import serializers

logger = logging.getLogger(__name__)


# Create your views here.


class FoodRecipeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        """
        API - to fetch food recipes with filtering by type (VEG, NON-VEG) and name search.
        {
            "status": "success",
            "message": "Food Recipe List",
            "data": [
                        {
                            "id": 1,
                            
                            "category": "VEG",
                            
                            "name": "Detox Rainbow Roll-Ups with Peanut Sauce",
                            
                            "description": "This is a rainbow roll-up that’s a nutritional powerhouse with foods like: carrots. chickpeas. curry. red cabbage. peanuts. dark leafy greens.",
                            
                            "ingredients": "3/4 cup peanut butter, 1/4 cup soy sauce (tamari or coconut aminos if gluten free), 1/4 cup rice vinegar, 1/4 cup water, 2 tablespoons honey, 1 clove garlic",
                            
                            "method": "1. Trim the stem/spine of the collard leaf – don’t cut it completely off, but just cut it down so that it’s nice and thin and pliable. 2.  Arrange your fillings on the collard leaf."
                        }
                    ]
        }
    
        """
        try:
            category = request.GET.get('category')
            id = request.GET.get('id')
            name = request.GET.get('name')
            user = request.GET.get('user')
            
            filter_dict = {}

            if category and category in ['VEG', 'NON-VEG']:     # filtering by type
                filter_dict['category'] = category
                
            if id:
                filter_dict['id'] = id
                
            if name: 
                filter_dict.update(name__icontains=name)   # recipe name search
                
            if user:
                filter_dict.update(user=user)   # user wise recipe search

            food_recipes = Recipe.objects.filter(**filter_dict).values() 

            
            if not food_recipes:    # will rise if no recipe found
                return Response({'status': 'fail', 'message': 'No recipes found.'}, status=status.HTTP_404_NOT_FOUND)

            response_data = list(food_recipes)

            return Response({'status': 'success', 'message': 'Food Recipe List', 'data': response_data})

        except Exception as e:
            logger.exception(f'Exception {e}')
            return Response({'status': 'fail', 'message': 'Something went wrong, try again later.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    
    def post(self, request):
        """
        API - to create a Food Recipe.
        Sample response:
            {
                "status": "success",
                "message": "Food recipe created successfully."
            } 
        
        """
        try:
            data = request.data
            serializer = RecipeSerializer(data=data)
            
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            validated_data.update(user_id=request.user.id)
            Recipe.objects.create(**validated_data)

            return Response({'status': 'success', 'message': 'Food recipe created successfully.'}, status=status.HTTP_201_CREATED)
        
        except serializers.ValidationError as e:
            logger.exception(f'Validation error: {e}')  # It will catch any validation errors raised by the serializer
            return Response({'status': 'fail', 'message': 'Validation error occurred.', 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            logger.exception(f'Exception {e}')
            return Response({'status': 'fail', 'message': 'Something went wrong, try again later.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    def patch(self, request):
        """
        # API - Update Food Recipe details
        # sample response
            {
                "status": "success",
                "message": "Food Recipe updated successfully"
            }
        """
        try:
            data = request.data
            recipe_id = data.get('id')
            
            if not recipe_id:
                return Response({'status': 'fail', 'message': 'Please enter the recipe id'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = RecipeSerializer(data=data, partial=True)

            if serializer.is_valid():
                recipe_data = serializer.validated_data
                
                Recipe.objects.filter(id=recipe_id).update(**recipe_data)
                return Response({'status': 'success', 'message': 'Food recipe updated successfully'}, status=status.HTTP_200_OK)

            return Response({'status': 'fail', 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except serializers.ValidationError as e:
            logger.exception(f'Validation error: {e}')  # It will catch any validation errors raised by the serializer
            return Response({'status': 'fail', 'message': 'Validation error occurred.', 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request):
        """
        # API - Update Food Recipe details
        # sample response
            {
                "status": "success",
                "message": "Food recipe deleted successfully"
            }
        """
        try:
            id = request.data['id']
            recipe_filter = Recipe.objects.filter(id=id)
            
            if recipe_filter.exists(): 
                recipe_filter.delete()
                return Response({'status': 'success', 'message': 'Food recipe deleted successfully'}, status=status.HTTP_200_OK)
            else: return Response({'status': 'fail', 'message': 'Given id does not match with existing recipes'}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception('Exception {}'.format(e.args))
            return Response({'status': 'fail', 'message': 'Something went wrong. Please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            