import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Body

from security import get_current_user

from schemas import IssueSchema, IssuesSchema
from schemas.request_params import OrderByQueryParamApp, OrderDirectionQueryParam
from services import IssueService, get_issue_service

router = APIRouter(
    prefix='/issue',
    tags=['issue'],
    dependencies=[Depends(get_current_user), ]
)


@router.get('', response_model=IssuesSchema)
async def read_all_issues_by_date(created_at: Annotated[datetime.date, Query(default_factory=datetime.date.today)],
                                  order_by: OrderByQueryParamApp = 'created_at',
                                  order_direction: OrderDirectionQueryParam = 'desc',
                                  issue_service: IssueService = Depends(get_issue_service)):
    issues = await issue_service.get_all_by_date(order_by, order_direction, created_at)
    return {'issues': issues}


@router.get('/{pk}', response_model=IssueSchema)
async def read_by_id(pk: int, issue_service: IssueService = Depends(get_issue_service)):
    issue = await issue_service.get_item_by_id(pk)
    return issue


@router.put('/{pk}', response_model=IssueSchema)
async def make_comment(pk: int, comment: str = Body('', embed=True),
                       issue_service: IssueService = Depends(get_issue_service)):
    commented_issue = await issue_service.make_comment(pk, comment)
    return commented_issue
