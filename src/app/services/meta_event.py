import hashlib
import logging
import os
import re
import time

import requests
from dotenv import find_dotenv, load_dotenv

from ..form import Contact

load_dotenv(find_dotenv())

test_event_code = os.getenv("META_TEST_EVENT_CODE")


def _normalize_phone(phone: str) -> str:
    return re.sub(r"\D", "", phone)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def send_meta_lead(contact: Contact):
    url = f"https://graph.facebook.com/v19.0/{os.getenv('META_PIXEL_ID')}/events"

    user_data = {
        "em": _sha256(contact.email.strip().lower()),
        "fn": _sha256(contact.first_name.strip().lower()),
        "ln": _sha256(contact.last_name.strip().lower()),
    }

    if contact.phone:
        normalized_phone = _normalize_phone(contact.phone)
        if normalized_phone:
            user_data["ph"] = _sha256(normalized_phone)

    payload = {
        "data": [
            {
                "event_name": "Lead",
                "event_time": int(time.time()),
                "event_id": contact.meta_event_id,
                "action_source": "website",
                "user_data": user_data,
            }
        ],
    }

    if test_event_code:
        payload["test_event_code"] = test_event_code

    response = requests.post(
        url,
        params={"access_token": os.getenv("META_SECRET_KEY")},
        json=payload,
        timeout=5,
    )

    if response.status_code != 200:
        raise Exception(f"Meta API error: {response.status_code} - {response.text}")

    logging.info(f"Meta lead sent successfully for event_id: {contact.meta_event_id}")
    return
