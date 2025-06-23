from typing import Annotated, List
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
load_dotenv(override=True)

from fastapi import Depends, Query, Request
import uvicorn

import util
from api import app
from auth import authentication
from service import \
    get_datasets, search_keywords, export_csv

@app.get("/datasets")
@authentication
async def get_datasets_controller(request: Request):
    return {
        'datasets': get_datasets()
    }

@app.get("/datasets/{dataset}/search")
@authentication
async def search_keywords_controller(request: Request, dataset: str, q: str):
    keywords = util.parse_list(q)
    return {
        'result': search_keywords(dataset, keywords)
    }

@app.get("/datasets/{dataset}/csv")
@authentication
async def export_csv_controller(request: Request, dataset: str):
    return StreamingResponse(iter([export_csv(dataset).getvalue()]), 
                             media_type='text/csv', headers={'Content-Disposition': 'attachment; filename=export.csv'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)