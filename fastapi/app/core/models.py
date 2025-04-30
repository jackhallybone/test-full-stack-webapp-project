from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

import app.projects.models
import app.item_settings.models
import app.items.models