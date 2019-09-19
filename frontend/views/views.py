from datetime import datetime, timezone

from django.http import JsonResponse
from django.utils.translation import gettext as _

from frontend.helpers import str_to_json
from frontend.models import Migration


def is_alive(request):
    alive_date = datetime.now(tz = timezone.utc)
    response_data = {'is_alive': 'yes', 'date': alive_date}
    return JsonResponse(response_data)


def validate_username(request):
    username = request.POST.get("username", None)
    data = {
        "is_taken": Migration.objects.filter(username__iexact = username).exists()
    }
    if data["is_taken"]:
        data["status"] = True
        data["error_message"] = _("A user with this username already exists.")

    return JsonResponse(data)


def validate_sponsor(request):
    form = request.POST.get("form", None)
    item = request.POST.get("item", None)
    data = {}
    is_taken = False

    if form is not None:
        form_data = str_to_json(form)

        sponsor = form_data['sponsor']
        placement_name = form_data['placement_name']
        if item == "sponsor":
            is_taken = Migration.objects.filter(username__exact = sponsor).exists()
        if item == "placement_name":
            is_taken = Migration.objects.filter(username__exact = placement_name).exists()
    else:
        data["form_error"] = _("No data submitted")

    if not is_taken:
        data["is_taken"] = is_taken
        data["status"] = True
        data["error_message"] = _("This sponsor doesn't exist")

    return JsonResponse(data)


def validate_email(request):
    email = request.POST.get("email", None)
    data = {
        "is_taken": Migration.objects.filter(email__exact = email).count()
    }
    if data["is_taken"] == 3:
        data["status"] = True
        data["error_message"] = _("This email has reached the maximum number of subscription")

    return JsonResponse(data)


def validate_placement_name(request):
    placement_name = request.POST.get("placement_name", None)
    data = {
        "is_taken": Migration.objects.filter(sponsor__exact = placement_name).count()
    }
    if data["is_taken"] == 2:
        data["status"] = True
        data["error_message"] = _("This sponsor can no longer support people")

    return JsonResponse(data)


def validate_placement_mode(request):
    placement_name = request.POST.get("placement_name", None)
    placement_mode = request.POST.get("placement_mode", None)
    if placement_mode in ["left", "right"]:
        data = {
            "is_taken": Migration.objects.filter(placement_name__exact = placement_name, placement_mode__exact = placement_mode).exists()
        }
        if data["is_taken"]:
            data["status"] = True
            data["error_message"] = _("This sponsor can no longer add people under this side")

        return JsonResponse(data)
