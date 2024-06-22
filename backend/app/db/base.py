# Import all the models, so that Base has them before being

from app.db.base_class import Base
from app.api.auth.db_models.user import User
from app.api.auth.db_models.tenant import Tenant
from app.api.product.db_models.product import Product
from app.api.product.db_models.product_type import ProductType
from app.api.product.db_models.company import Company

