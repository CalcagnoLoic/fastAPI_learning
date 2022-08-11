from fastapi import FastAPI, APIRouter

# 1. On crée une liste de dictionnaire
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


# 2. On crée un nouvel endpoint en capturant un ID
# 3. On simule le fetch des data par ID. Le résultat est sérialisé et retourné en JSON par FastAPI
@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
