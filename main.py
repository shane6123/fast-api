from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# get route for test 
@app.get("/test")
async def test():
    return {"message": "Hello for test"}

# post route for test and return body data 
@app.post("/test")
async def test(data: dict):
    return {"message": data}


