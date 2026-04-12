import logging

from fastapi.responses import JSONResponse

from ..services import confirmation_email, send_email_to_admin, send_meta_lead
from .model import Contact


def submit_contact_form(form_data: Contact) -> JSONResponse:
    try:
        send_email_to_admin(form_data)
        confirmation_email(form_data.first_name, form_data.email)
    except Exception as e:
        logging.error(f"Error occurred for {form_data.email}: {e}")
        return JSONResponse(
            content={"message": "An error occurred while submitting the form"},
            status_code=500,
        )

    if form_data.meta_event_id:
        try:
            send_meta_lead(form_data)
        except Exception as e:
            logging.error(f"Failed to send meta lead for {form_data.email}: {e}")

    logging.info(f"Contact form submitted successfully for {form_data.email}")
    return JSONResponse(
        content={"message": "Form submitted successfully"},
        status_code=201,
    )
