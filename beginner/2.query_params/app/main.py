from typing import Optional
from fastapi import FastAPI, APIRouter


RECIPES = [
    {
      "id": 1,
      "label": "Chicken Vesuvio",
      "source": "Serious Eats",
      "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()

@api_router.get("/", status_code=200)
def root() -> dict:
    return {"msg": "Hello, World!"}


@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


# 1. On crée une nouvelle route sans paramètre.
@api_router.get("/search/", status_code=200)
def search_recipes(keyword: Optional[str] = None, max_results: Optional[int] = 10):
    """
    Cette fonction permet de définir la logique de l'endpoint via 2 query utilisé en tant que paramètre. On précise le
    type et la valeur par défaut de chaque argument ainsi que le caractère non obligatoire de ces arguments.
    La request est dans ce style : http://127.0.0.1:8000/search/?keyword=chick&max_results=1
    """
    if not keyword:
        return {"results": RECIPES[:max_results]}
    results = filter(lambda recipe: keyword.lower() in recipe['label'].lower(), RECIPES)
    return {"results": list(results)[:max_results]}



app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")