import json

from recipes import models


f = open('main_recipes_tagrecipe.json', 'r')
data = json.load(f)
for i in data:
    recipe = models.Recipe.objects.get(pk=i['recipe_id'])
    tag = models.Tag.objects.get(pk=i['tag_id'])
    models.TagRecipe.objects.create(
        recipe=recipe,
        tag=tag,
    )
f.close()

f = open('main_recipes_ingredientrecipe.json', 'r')
data = json.load(f)
for i in data:
    ingredient = models.Ingredient.objects.get(pk=i['ingredient_id'])
    recipe = models.Recipe.objects.get(pk=i['recipe_id'])
    models.IngredientRecipe.objects.create(
        ingredient=ingredient,
        recipe=recipe,
        amount=i['amount'],
    )
f.close()
