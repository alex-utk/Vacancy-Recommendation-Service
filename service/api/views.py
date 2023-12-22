from typing import List

from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel
from ..utils import get_from_db
from ..db_classes import Vacancies, Resumes

import pandas as pd


class Responce(BaseModel):
    results: List[dict]

router = APIRouter()


@router.get(path="/health")
async def health() -> str:
    return "I am alive"


@router.post(path="/get_vacancies", response_model=Responce)
async def recomend_vacancies(request: Request) -> Responce:
    data = await request.json()

    encoder = request.app.state.encoder
    ann = request.app.state.ann

    all_text = f"{data['vacancy']} {data['city_name']} {data['description']}"

    embedding = encoder.encode(all_text, normalize_embeddings=True)
    vacancy_ids, _ = ann['vacanсies'].knnQuery(embedding, k=5)
    vacancy_ids = vacancy_ids.tolist()

    results = get_from_db(request.app.state.db_engine, vacancy_ids, Vacancies)

    results_list = [
        {'custom_position': result.custom_position,
         'experience': result.experience,
         'salary': result.salary,
         'city_name': result.city_name,
        }
        for result in results
    ]

    results_df = pd.DataFrame.from_dict(results_list)
    results_df['experience_diff'] = abs(results_df['experience'] - data['experience'])
    results_df['salary_diff'] = abs(results_df['salary'] - data['salary'])
    results_df['is_true_city'] = results_df['city_name'] == data['city_name']
    results_df = results_df.sort_values(by=['is_true_city', 'experience_diff', 'salary_diff'],
                                        ascending=[False, True, True])

    results_list = (results_df
                    .drop(columns=['experience_diff', 'is_true_city', 'salary_diff'])
                    .to_dict('records'))

    return {'results': results_list}


@router.post(path="/get_resumes", response_model=Responce)
async def recomend_resumes(request: Request) -> Responce:
    data = await request.json()

    encoder = request.app.state.encoder
    ann = request.app.state.ann

    all_text = f"{data['vacancy']} {data['city_name']} {data['description']}"

    embedding = encoder.encode(all_text, normalize_embeddings=True)
    vacancy_ids, _ = ann['resumes'].knnQuery(embedding, k=5)
    vacancy_ids = vacancy_ids.tolist()

    results = get_from_db(request.app.state.db_engine, vacancy_ids, Resumes)

    results_list = [
        {'employee_description': result.description,
         'vacancy': result.vacancy,
         'salary': result.salary,
         'education': result.education,
         'city_name': result.city_name,
        }
        for result in results
    ]

    results_df = pd.DataFrame.from_dict(results_list)

    results_df['is_true_city'] = results_df['city_name'] == data['city_name']
    results_df = results_df.sort_values(by=['is_true_city', 'salary'],
                                        ascending=[False, True])

    results_list = results_df.drop(columns=['is_true_city']).to_dict('records')

    return {'results': results_list}


def add_views(app: FastAPI) -> None:
    app.include_router(router)
