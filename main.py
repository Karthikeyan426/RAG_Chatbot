from fastapi import FastAPI
from chats import chat_api
from users import users_api
from docs import docs_api
from database_config import lifespan

app = FastAPI(lifespan = lifespan)

@app.get('/')
async def root():
    return 'server running'

app.include_router(chat_api.router)
app.include_router(users_api.router)
app.include_router(docs_api.router)
