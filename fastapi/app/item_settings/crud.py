from app.core.crud import CRUDBase
from app.item_settings.models import ItemStatus, ItemLocation, ItemType
from app.item_settings.schemas import ItemStatusCreate, ItemStatusUpdate, ItemLocationCreate, ItemLocationUpdate, ItemTypeCreate, ItemTypeUpdate


class CRUDItemStatus(CRUDBase[ItemStatus, ItemStatusCreate, ItemStatusUpdate]):
    pass

class CRUDItemLocation(CRUDBase[ItemLocation, ItemLocationCreate, ItemLocationUpdate]):
    pass

class CRUDItemType(CRUDBase[ItemType, ItemTypeCreate, ItemTypeUpdate]):
    pass


item_status_crud = CRUDItemStatus(ItemStatus)
item_location_crud = CRUDItemStatus(ItemLocation)
item_type_crud = CRUDItemStatus(ItemType)
