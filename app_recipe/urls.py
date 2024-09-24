from django.urls import path
from app_recipe.views import FoodRecipeView

urlpatterns = [
    path('recipe/', FoodRecipeView.as_view())
]
