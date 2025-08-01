# context_model.py

from pydantic import BaseModel

# 📦 Shared context for all agents
class UserContext(BaseModel):
    name: str
    is_premium_user: bool
    issue_type: str
