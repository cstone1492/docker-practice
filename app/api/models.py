from uuid import UUID
from pydantic import BaseModel, Field, constr
from typing import Annotated, Union


UUID_FAIL = UUID("00000000-0000-0000-0000-000000000000")

class BaseRepsonse(BaseModel):
    """
    Contians base success criterion and response
    """

    success: Annotated[
        bool,
        Field(description="Activity was successful (true) or failed (false)",
              examples=[True]
              ), ] = False
    status_text: Annotated[
        constr(min_length=2, max_length=1024),
        Field(description="Textual context for success code",
              examples=["No error, no context"]
              ), ] = "Uninitialized error condition"