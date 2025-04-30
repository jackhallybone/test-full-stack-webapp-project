from app.core.crud import CRUDBase
from app.items.models import Item
from app.items.schemas import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item_crud = CRUDItem(Item)
