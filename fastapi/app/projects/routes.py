from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.projects.crud import project_crud
from app.projects.models import Project
from app.projects.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()


@router.post("/projects/", response_model=ProjectRead)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)) -> Project:
    return await project_crud.create(db=db, data=data)


@router.get("/projects/", response_model=list[ProjectRead])
async def get_projects(db: AsyncSession = Depends(get_db)) -> list[Project]:
    return await project_crud.read_many(db=db)


@router.get("/projects/{id}", response_model=ProjectRead)
async def get_project(id: int, db: AsyncSession = Depends(get_db)) -> Project:
    return await project_crud.read_one(db=db, id=id)


@router.put("/projects/{id}", response_model=ProjectRead)
async def update_project(id: int, data: ProjectUpdate, db: AsyncSession = Depends(get_db)) -> Project:
    return await project_crud.update(db=db, id=id, data=data)


@router.delete("/projects/{id}", status_code=204)
async def delete_project(id: int, db: AsyncSession = Depends(get_db)) -> None:
    return await project_crud.delete(db=db, id=id)
