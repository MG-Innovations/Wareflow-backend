# Import all the models, so that Base has them before being

from db.base_class import Base
from api.auth.models.user import User
from api.auth.models.tenant import Tenant
