from typing import Literal, Optional

from pydantic import BaseModel


class ArchivoSubidoResponse(BaseModel):
	asset_kind: Literal["imagen", "documento"]
	url: str
	secure_url: str
	public_id: Optional[str] = None
	resource_type: str
	format: Optional[str] = None
	bytes: Optional[int] = None
	original_filename: Optional[str] = None
	mime_type: str
	folder: Optional[str] = None
	uploaded_by: int
