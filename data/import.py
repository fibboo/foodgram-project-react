import json

from recipes.models import Ingredient

f = open('ingredients.json', 'r')
data = json.load(f)

for i in data:
    Ingredient.objects.create(
        name=i['name'],
        measurement_unit=i['measurement_unit']
    )

f.close()
