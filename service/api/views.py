from typing import List

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from ..utils import get_from_db
from ..db_classes import Vacancies, Resumes

from service.api.exceptions import ModelNotFoundError, UserNotFoundError, WrongTokenError
from service.log import app_logger
import numpy as np


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


class RecruterResponce():
    pass

class WorkerResponce():
    pass

router = APIRouter()
# bearer = HTTPBearer()

@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


# @router.get(
#     path="/{model_name}/{user_id}",
#     response_model=RecoResponse
# )
# async def get_reco(request: Request, model_name: str, user_id: int, token: str = Depends(bearer)) -> RecoResponse:
#     app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

#     k_recs = request.app.state.k_recs
#     models = request.app.state.models
#     true_token = request.app.state.true_token

#     auth_token = token.credentials

#     if auth_token != true_token:
#         raise WrongTokenError()

#     if user_id > 10**9:
#         raise UserNotFoundError(error_message=f"User {user_id} not found")

#     if model_name not in request.app.state.models:
#         raise ModelNotFoundError(error_message=f"Model {model_name} not found")

#     reco = models[model_name].get_reco(user_id, k_recs)

#     return RecoResponse(user_id=user_id, items=reco)

@router.post(path="/get_vacancies")
async def recomend_vacancies(request: Request):
    data = await request.json()

    encoder = request.app.state.encoder
    ann = request.app.state.ann

    embedding = encoder.encode(data['description'], normalize_embeddings=True)
    vacancy_ids, _ = ann['vacanсies'].knnQuery(embedding, k=5)
    vacancy_ids = vacancy_ids.tolist()

    results = get_from_db(request.app.state.db_engine, vacancy_ids, Vacancies)

    results_list = [(result.custom_position, result.experience, result.salary, result.city_name)
                    for result in results]

    # print(type(vacancy_ids))
    # print(vacancy_ids)
    # print(len(results))
    # # return 0
    return {'results': results_list}


@router.post(path="/get_resumes")
async def recomend_resumes(request: Request):
    data = await request.json()

    encoder = request.app.state.encoder
    ann = request.app.state.ann

    embedding = encoder.encode(data['description'], normalize_embeddings=True)
    vacancy_ids, _ = ann['resumes'].knnQuery(embedding, k=5)
    vacancy_ids = vacancy_ids.tolist()

    results = get_from_db(request.app.state.db_engine, vacancy_ids, Resumes)

    results_list = [(result.description, result.vacancy, result.salary, result.education, result.city_name)
                    for result in results]
    return {'results': results_list}


def add_views(app: FastAPI) -> None:
    app.include_router(router)
