from django.shortcuts import render
import uuid

# Registers session cookie and gives template
def index(request):
    user_id = uuid.uuid4().hex
    request.session["user_uuid"] = user_id
    
    return render(
        request,
        "../templates/index.html"
    )