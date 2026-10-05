from fastapi import FastAPI

app = FastAPI(
    title="EduConnect",
    description="API para gerenciamento escolar",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo ao EduConnect"
    }