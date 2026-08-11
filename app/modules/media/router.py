from fastapi import APIRouter, Depends, File, UploadFile

from app import auth
from app.core.cloudinary_storage import upload_media_file

from . import schemas


router = APIRouter(prefix="/media")


@router.post("/subir/", response_model=schemas.ArchivoSubidoResponse, tags=["Media"])
async def subir_archivo(
	file: UploadFile = File(...),
	current_user=Depends(auth.get_current_user),
):
	return await upload_media_file(file=file, uploaded_by=current_user.id_usuario)