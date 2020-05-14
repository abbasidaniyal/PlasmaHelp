from datetime import datetime

from plasma_for_covid import settings
from users.utils import send_mail


def send_query(request, query):
    send_mail(
        "A new query from PlasmaHelp Website",
        f"""
Name : {query.name}
Email : {query.email}
Contact Number : {query.contact_number}
DateTime : {datetime.now()} UTC
Query : {query.query}
        """,
        f"{query.email}",
        [f"{settings.EMAIL_HOST_USER}"],
        fail_silently=True,
    )
