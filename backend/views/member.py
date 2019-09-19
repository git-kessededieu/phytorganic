from django.http import JsonResponse
from django.utils.translation import gettext as _

from backend.models import Member


def store_username(request, **kwargs):
    print(kwargs)
    pass


def validate_username(request):
    f_username = request.POST.get("username", None)
    data = {}

    member = Member.objects.filter(username__iexact = f_username).exists()

    if not member:
        data["status"] = True
        data["messages"] = []
    else:
        data["status"] = False
        data["messages"] = [_("A user with this username already exists.")]

    return JsonResponse(data)


def validate_email(request):
    f_email = request.POST.get("email", None)
    data = {}

    member_count = Member.objects.filter(email__exact = f_email).count()

    if member_count <= 2:
        data["status"] = True
        data["messages"] = []
    elif member_count >= 3:
        data["status"] = False
        data["messages"] = [_("This email has reached the maximum number of subscription")]

    return JsonResponse(data)


def validate_sponsor(request):
    f_sponsor = request.POST.get("sponsor", None)
    data = {}

    member = Member.objects.filter(username__iexact = f_sponsor).first()

    if not member:
        data["status"] = False
        data["messages"] = [_("This sponsor doesn't exist")]
    else:
        data["status"] = True
        data["messages"] = [member.full_name]

    return JsonResponse(data)


def validate_placement_name(request):
    f_placement_name = request.POST.get("placement_name", None)
    data = {}

    member = Member.objects.filter(username__exact = f_placement_name).first()
    member_count = Member.objects.filter(placement_name__exact = f_placement_name).count()

    if not member:
        data["status"] = False
        data["messages"] = [_("This member doesn't exist")]
    else:
        data["status"] = True
        data["messages"] = [member.full_name]
    if member_count == 2:
        data["status"] = False
        data["messages"].append(_("This sponsor can no longer support people"))

    return JsonResponse(data)


def validate_placement_mode(request):
    f_placement_name = request.POST.get("placement_name", None)
    f_placement_mode = request.POST.get("placement_mode", None)
    data = {}
    if f_placement_mode in ["left", "right"]:
        member = Member.objects.filter(placement_name__exact = f_placement_name,
                                       placement_mode__exact = f_placement_mode).exists()

        if not member:
            data["status"] = True
            data["messages"] = []
        else:
            data["status"] = False
            data["messages"] = [_("This sponsor can no longer add people under this side")]

        return JsonResponse(data)


def get_member(request, **kwargs):
    username = kwargs.get('username', '')
    try:
        r_member = Member.objects.get(username__iexact = username)
        member = {
            "username": r_member.username,
            "last_name": r_member.last_name,
            "first_name": r_member.first_name,
        }
    except Member.DoesNotExist:
        member = None

    return JsonResponse(member, safe = False)
