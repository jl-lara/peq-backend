from __future__ import annotations

import base64
import json
import mimetypes
import os
import uuid
from pathlib import Path
from typing import Literal
from urllib import error, request
from urllib.parse import urlparse

from fastapi import HTTPException, UploadFile, status
from dotenv import load_dotenv

load_dotenv()

ASSET_KIND_IMAGE = "imagen"
ASSET_KIND_DOCUMENT = "documento"

IMAGE_EXTENSIONS = {
	".jpg",
	".jpeg",
	".png",
	".webp",
	".gif",
	".bmp",
	".tif",
	".tiff",
	".avif",
	".heic",
	".heif",
}

DOCUMENT_EXTENSIONS = {
	".pdf",
	".doc",
	".docx",
	".xls",
	".xlsx",
	".csv",
	".ppt",
	".pptx",
	".txt",
	".rtf",
	".odt",
	".ods",
	".odp",
}

MAX_IMAGE_SIZE = 20 * 1024 * 1024
MAX_DOCUMENT_SIZE = 50 * 1024 * 1024


def _get_env_value(name: str) -> str:
	value = os.getenv(name, "").strip()
	if not value:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Falta configurar la variable de entorno {name}.",
		)
	return value


def _cloudinary_credentials() -> tuple[str, str, str]:
	cloudinary_url = os.getenv("CLOUDINARY_URL", "").strip()
	if cloudinary_url:
		parsed_url = urlparse(cloudinary_url)
		if parsed_url.scheme != "cloudinary" or not parsed_url.hostname or not parsed_url.username or not parsed_url.password:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="CLOUDINARY_URL tiene un formato inválido. Debe ser cloudinary://api_key:api_secret@cloud_name.",
			)
		return parsed_url.hostname, parsed_url.username, parsed_url.password

	cloud_name = _get_env_value("CLOUDINARY_CLOUD_NAME")
	api_key = _get_env_value("CLOUDINARY_API_KEY")
	api_secret = _get_env_value("CLOUDINARY_API_SECRET")
	return cloud_name, api_key, api_secret


def _guess_mime_type(file_name: str | None, declared_mime: str | None) -> str:
	if declared_mime:
		return declared_mime
	if file_name:
		mime_type, _ = mimetypes.guess_type(file_name)
		if mime_type:
			return mime_type
	return "application/octet-stream"


def _detect_asset_kind(file_name: str | None, mime_type: str) -> Literal["imagen", "documento"]:
	file_extension = Path(file_name or "").suffix.lower()

	if mime_type.startswith("image/") or file_extension in IMAGE_EXTENSIONS:
		return ASSET_KIND_IMAGE

	if file_extension in DOCUMENT_EXTENSIONS or mime_type in {
		"application/pdf",
		"application/msword",
		"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
		"application/vnd.ms-excel",
		"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		"application/vnd.ms-powerpoint",
		"application/vnd.openxmlformats-officedocument.presentationml.presentation",
		"text/plain",
		"text/csv",
	}:
		return ASSET_KIND_DOCUMENT

	raise HTTPException(
		status_code=status.HTTP_400_BAD_REQUEST,
		detail="Solo se permiten imágenes o documentos compatibles.",
	)


def _build_multipart_form(fields: dict[str, str], file_field: str, file_name: str, file_bytes: bytes, mime_type: str) -> tuple[bytes, str]:
	boundary = uuid.uuid4().hex
	parts: list[bytes] = []

	for key, value in fields.items():
		parts.append(f"--{boundary}\r\n".encode())
		parts.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
		parts.append(value.encode())
		parts.append(b"\r\n")

	parts.append(f"--{boundary}\r\n".encode())
	parts.append(
		f'Content-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'.encode()
	)
	parts.append(f"Content-Type: {mime_type}\r\n\r\n".encode())
	parts.append(file_bytes)
	parts.append(b"\r\n")
	parts.append(f"--{boundary}--\r\n".encode())

	return b"".join(parts), boundary


async def upload_media_file(file: UploadFile, uploaded_by: int | None = None) -> dict:
	cloud_name, api_key, api_secret = _cloudinary_credentials()
	file_name = file.filename or "archivo"
	mime_type = _guess_mime_type(file_name, file.content_type)
	asset_kind = _detect_asset_kind(file_name, mime_type)
	file_bytes = await file.read()
	file_size = len(file_bytes)

	if asset_kind == ASSET_KIND_IMAGE and file_size > MAX_IMAGE_SIZE:
		raise HTTPException(
			status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
			detail="La imagen excede el tamaño máximo permitido de 20 MB.",
		)

	if asset_kind == ASSET_KIND_DOCUMENT and file_size > MAX_DOCUMENT_SIZE:
		raise HTTPException(
			status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
			detail="El documento excede el tamaño máximo permitido de 50 MB.",
		)

	resource_type = "image" if asset_kind == ASSET_KIND_IMAGE else "raw"
	folder_suffix = uploaded_by if uploaded_by is not None else "publico"
	folder = f"peq/{'imagenes' if asset_kind == ASSET_KIND_IMAGE else 'documentos'}/{folder_suffix}"
	cloudinary_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/{resource_type}/upload"
	form_fields = {
		"folder": folder,
		"use_filename": "true",
		"unique_filename": "true",
		"overwrite": "false",
	}
	body, boundary = _build_multipart_form(
		fields=form_fields,
		file_field="file",
		file_name=file_name,
		file_bytes=file_bytes,
		mime_type=mime_type,
	)
	credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
	request_headers = {
		"Authorization": f"Basic {credentials}",
		"Content-Type": f"multipart/form-data; boundary={boundary}",
	}

	req = request.Request(cloudinary_url, data=body, headers=request_headers, method="POST")

	try:
		with request.urlopen(req, timeout=60) as response:
			payload = json.loads(response.read().decode("utf-8"))
	except error.HTTPError as exc:
		response_body = exc.read().decode("utf-8", errors="ignore")
		try:
			error_payload = json.loads(response_body)
			message = error_payload.get("error", {}).get("message") or response_body or "Error desconocido"
		except json.JSONDecodeError:
			message = response_body or "Error desconocido"
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"Cloudinary rechazó la subida: {message}",
		) from exc
	except error.URLError as exc:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail=f"No fue posible conectar con Cloudinary: {exc.reason}",
		) from exc

	secure_url = payload.get("secure_url") or payload.get("url")
	if not secure_url:
		raise HTTPException(
			status_code=status.HTTP_502_BAD_GATEWAY,
			detail="Cloudinary no devolvió una URL válida para el archivo subido.",
		)

	return {
		"asset_kind": asset_kind,
		"url": secure_url,
		"secure_url": secure_url,
		"public_id": payload.get("public_id"),
		"resource_type": payload.get("resource_type", resource_type),
		"format": payload.get("format"),
		"bytes": payload.get("bytes"),
		"original_filename": payload.get("original_filename", file_name),
		"mime_type": mime_type,
		"folder": payload.get("folder", folder),
		"uploaded_by": uploaded_by or 0,
	}