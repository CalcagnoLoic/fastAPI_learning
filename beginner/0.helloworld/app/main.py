from fastapi import FastAPI, APIRouter

# 1. On instancie un object FastAPI donnant toutes les fonctionnalités de fastAPI
app = FastAPI(
    title="Recipe Api", openapi_url="/openapi.json"
)

# 2. On instancie un routeur fastAPI regroupant les endpoints
api_router = APIRouter()


# 3. Ajout d'un décorateur pour définir un endpoint avec un GET
@api_router.get("/", status_code=200)
def root() -> dict:
    return {"msg": "Hello, World!"}


# 4. On utilise une méthode pour enregistrer la route
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

