import uvicorn
from fastapi import FastAPI

app = FastAPI()
hits = 0

@app.get("/metric")
async def metric():
    global hits
    hits+=1
    return {"hits": hits}

@app.get("/health")
async def health():
    return "ok"
    
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)