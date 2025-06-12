from fastapi import FastAPI
from src.accounts.routes import router as accounts_router
from src.movies.routes import router as movies_router
from src.cart.routes import router as cart_router
from src.orders.routes import router as orders_router
from src.payments.routes import router as payments_router

app = FastAPI(title="Online Cinema")

app.include_router(accounts_router)
app.include_router(movies_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(payments_router)

@app.get("/")
def root():
    return {"msg": "Hello from Online Cinema!"}
