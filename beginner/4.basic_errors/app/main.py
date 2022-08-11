from typing import Optional
from fastapi import FastAPI, APIRouter, Query, HTTPException
from schema import Recipe, RecipeSearchResults, RecipeCreate

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


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Fetch a single recipe by ID
    """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]

    # 1. On capture une exception
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} is not found"
        )
    return result[0]


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
        *,
        keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
        max_results: Optional[int] = 10
) -> dict:
    """
    Cette fonction permet de définir la logique de l'endpoint via 2 query utilisé en tant que paramètre. On précise le
    type et la valeur par défaut de chaque argument ainsi que le caractère non obligatoire de ces arguments.
    La request est dans ce style : http://127.0.0.1:8000/search/?keyword=chick&max_results=1
    """
    if not keyword:
        return {"results": RECIPES[:max_results]}
    results = filter(lambda recipe: keyword.lower() in recipe['label'].lower(), RECIPES)
    return {"results": list(results)[:max_results]}


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate):
    """
    Creation of a new recipe
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url
    )
    RECIPES.append(recipe_entry.dict())
    return recipe_entry


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
