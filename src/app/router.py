import logging
import os
import subprocess
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .config import limiter
from .form import Contact, submit_contact_form
from .services import ClientError

router = APIRouter()
logger = logging.getLogger(__name__)


def get_client_ip(request: Request) -> Optional[str]:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.client.host if request.client else None


@router.post("/submit_form")
@limiter.limit("5/minute")
async def submit_form(request: Request, form_data: Contact) -> JSONResponse:
    logging.info(f"Received contact form submission from {form_data.email}")

    client_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent")

    return submit_contact_form(form_data, client_ip, user_agent)


@router.post("/client-error")
def client_error(request: Request, payload: ClientError):
    """Endpoint to receive client-side error reports from the frontend."""
    route = "meta" if payload.isMetaRoute else "organic"
    user_agent = request.headers.get("user-agent")

    discord_script_path = os.environ.get("DISCORD_SCRIPT_PATH")

    if not discord_script_path:
        logger.warning("DISCORD_SCRIPT_PATH is not set")
        return {"ok": True}

    details = f"{payload.message}\nURL: {payload.url or 'N/A'}\nRoute: {route}\nCookies: {payload.hasCookieConsent or 'N/A'}\nReferrer: {payload.referrer or 'N/A'} \n User Agent: {user_agent or 'N/A'}"
    if payload.stack:
        details += f"\nStack: {payload.stack[:300]}"

    try:
        subprocess.run(
            [
                discord_script_path,
                "FRONT",
                "ERROR",
                details,
            ],
            check=False,
        )
    except Exception:
        logger.exception("Failed to send Discord alert")
        logger.error(
            f"[FRONT][{route}] {payload.message} | url={payload.url} | cookies={payload.hasCookieConsent} | referrer={payload.referrer} | ua={user_agent}"
        )

    return {"ok": True}
