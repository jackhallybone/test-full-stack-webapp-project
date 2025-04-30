from app.core.crud import CRUDBase
from app.projects.models import Project
from app.projects.schemas import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass


project_crud = CRUDProject(Project)
