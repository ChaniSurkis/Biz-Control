import sys
from pathlib import Path

# מוסיף את /app ל-PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.database import Base
from app.models.user import User
from app.models.appointment import Appointment

from alembic import context

target_metadata = Base.metadata
