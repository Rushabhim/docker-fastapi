from fastapi import FastAPI

from app.db import database, User

import pandas as pd
from fastapi import FastAPI, Response
import gzip
import io
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
        
        
# @app.post('/file')
# async def file_endpoint(data: pd.DataFrame):
#     # convert the dataframe to csv and compress it
#     csv_bytes = data.to_csv(index=False).encode('utf-8')
#     compressed_data = zlib.compress(csv_bytes)

#     # create the response object with compressed data and appropriate headers
#     response = Response(content=compressed_data, media_type='application/octet-stream')
#     response.headers['Content-Disposition'] = 'attachment; filename="data.csv.gz"'
#     response.headers['Content-Encoding'] = 'gzip'
#     response.headers['Access-Control-Allow-Origin'] = '*'

#     return response

@app.post("/file")
def create_file(data: dict):
    df = pd.DataFrame(data["data"])
    output = io.StringIO()
    with gzip.GzipFile(fileobj=output, mode="w") as gz_file:
        df.to_csv(gz_file, index=False)
    compressed_data = output.getvalue().encode("utf-8")
    return JSONResponse(content=jsonable_encoder(compressed_data), media_type="application/octet-stream")