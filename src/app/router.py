import logging

from config import check_authentication
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from form import Contact, submit_contact_form

router = APIRouter()


@router.post("/submit_form")
async def submit_form(
    form_data: Contact, auth: None = Depends(check_authentication)
) -> JSONResponse:
    logging.info(f"Received contact form submission from {form_data.email}")
    return submit_contact_form(form_data)
