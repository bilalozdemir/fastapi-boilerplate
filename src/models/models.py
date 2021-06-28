from typing import Optional

from pydantic import BaseModel, StrictStr

class RouterRequest(BaseModel):
    name: Optional[StrictStr]
