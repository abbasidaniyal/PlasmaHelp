import os

from django.db.utils import IntegrityError
from users.models import User

try:
    User.objects.create_superuser(
        os.environ.get("ADMIN_USERNAME"), os.environ.get("ADMIN_PASSWORD")
    )
except IntegrityError:
    pass

exit()
