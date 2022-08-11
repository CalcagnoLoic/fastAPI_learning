from pathlib import Path
from typing import Optional, Any
from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from schema import Recipe, RecipeSearchResults, RecipeCreate
from recipe_data import RECIPES


# 1. On définit le template Jinja
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


# 2. On met à jour l'endpoint de base pour afficher les résultats de l'API dans notre template HTML.
@api_router.get("/", status_code=200)
def root(request: Request) -> _TemplateResponse:
    """
    Fonction permettant d'afficher les résultats de l'API. L'instanciation de la response prend en premier argument
    le template et en second argument, un dictionnaire avec les objets de la request ainsi que les variables du
    template
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": RECIPES},
    )


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Fetch a single recipe by ID
    """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]

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
