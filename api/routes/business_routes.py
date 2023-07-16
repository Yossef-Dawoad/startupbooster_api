import asyncio
from typing import Any

from fastapi import APIRouter

from ..utils import generate_business_snippet, generate_keywords

router = APIRouter(
    prefix="/api/v1",
    tags=["Businesses w/out DataBase"],
)
################################ api/ver 1 - no database ######################

StringArray = list[str]


@router.get("/keywords")
async def api_generate_keywords(prompt: str) -> dict[str, StringArray]:
    llm_result = await generate_keywords(prompt)
    return llm_result


@router.get("/snippets")
async def api_generate_snippets(prompt: str) -> str:
    llm_result = await generate_business_snippet(prompt)
    return llm_result


@router.get("/business")
async def api_generate_business_seo(prompt: str) -> dict[str, Any]:
    brandMaker_funcs = [generate_business_snippet, generate_keywords]
    tasks = [  # Wait for the tasks to finish using asyncio.gather()
        asyncio.create_task(func(prompt)) for func in brandMaker_funcs
    ]
    results = await asyncio.gather(*tasks)
    results_dict = {
        func.__name__: result for func, result in zip(brandMaker_funcs, results)
    }
    return {
        "snippet": results_dict["generate_business_snippet"],
        "keywords": results_dict["generate_keywords"]["kw"],
    }
