from  fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def f_index():
    return {"surname": "Калинин", "name": "Игорь", "patronymic": "Михайлович"}

@app.get('/tools')
async def f_indexT():
    return {"phone": "8-961-989-10-89", "tg": "t.me/Accretion_Ghost", "vk": "vk.com/igorkalinin2015"}


@app.get('/users')
async def f_indexT():
    return "bruh"