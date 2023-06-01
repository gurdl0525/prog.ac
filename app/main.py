from fastapi import FastAPI
import uvicorn

from app.model.sessionRequest import sessionRequest
from app.programmers.crawler import getUsers, getLevelCnt

app = FastAPI()


@app.post("/programmers/data")
async def root(request: sessionRequest):

    return {
        'user_info': getUsers(request.session_key),
        'level_count_list': getLevelCnt(request.session_key)
    }

if __name__ == '__main__':
    uvicorn.run(app)
