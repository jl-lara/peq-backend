from fastapi import APIRouter, File, UploadFile

from app.core.cloudinary_storage import upload_media_file

from . import schemas


router = APIRouter(prefix="/media")


@router.post("/subir/", response_model=schemas.ArchivoSubidoResponse, tags=["Media"])
async def subir_archivo(
	file: UploadFile = File(...),
):
	return await upload_media_file(file=file)