from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import uuid

# Registers session cookie and gives template
def index(request):
    user_id = uuid.uuid4().hex
    request.session["user_uuid"] = user_id
    
    return render(
        request,
        Path(settings.BASE_DIR).resolve().joinpath("backend/templates/index.html")
    )