from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test the publicly avaiable ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access endpoint"""

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "password")
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieveing a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Salt")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that the ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user("test2@test.com", "password")
        Ingredient.objects.create(user=user2, name="Vinegar")
        Ingredients = Ingredient.objects.create(user=self.user, name="Tumeric")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], Ingredients.name)

    def test_create_ingredient_successful(self):
        """Test if creating ingredient is successful"""
        payload = {"name": "Cabbage"}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.object.filter(user=self.user, name=payload["name"]).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test if creating an ingredient is failed"""
        payload = {}
        res = self.client.post(INGREDIENT_URL, payload)
        self.client(res.status_code, status.HTTP_400_BAD_REQUEST)
