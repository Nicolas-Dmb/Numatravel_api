import logging
import os
import subprocess

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .config import limiter
from .form import Contact, submit_contact_form
from .services import ClientError

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/submit_form")
@limiter.limit("5/minute")
async def submit_form(request: Request, form_data: Contact) -> JSONResponse:
    logging.info(f"Received contact form submission from {form_data.email}")
    return submit_contact_form(form_data)


@router.post("/client-error")
def client_error(payload: ClientError):
    """Endpoint to receive client-side error reports from the frontend."""
    logger.error(f"[FRONT] {payload.message}")

    discord_script_path = os.environ.get("DISCORD_SCRIPT_PATH")

    if not discord_script_path:
        logger.warning("DISCORD_SCRIPT_PATH is not set")
        return {"ok": True}

    try:
        subprocess.run(
            [
                discord_script_path,
                "FRONT",
                "ERROR",
                payload.message,
            ],
            check=False,
        )
    except Exception:
        logger.exception("Failed to send Discord alert")

    return {"ok": True}
