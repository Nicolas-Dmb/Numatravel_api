import logging

from config import limiter
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from form import Contact, submit_contact_form

router = APIRouter()


@router.post("/submit_form")
@limiter.limit("5/minute")
async def submit_form(request: Request, form_data: Contact) -> JSONResponse:
    logging.info(f"Received contact form submission from {form_data.email}")
    return submit_contact_form(form_data)
