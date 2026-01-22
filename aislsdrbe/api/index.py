from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="off")

__all__ = ["handler"]