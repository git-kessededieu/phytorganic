from django.http import JsonResponse
from django.utils.translation import gettext as _
from werkzeug.security import check_password_hash

from backend import logger
from backend.models import Member, Pack
from frontend.helpers import str_to_json
from frontend.models import Migration
from wallet.models import MemberWallet


def validate_username(request):
    f_username = request.POST.get("username", None)
    data = {}

    username = Member.objects.filter(username__iexact = f_username).exists()

    if not username:
        data["status"] = True
        data["messages"] = []
    else:
        data["status"] = False
        data["messages"] = [_("A user with this username already exists.")]

    return JsonResponse(data)


def get_member_activation(request):
    f_username = request.POST.get("username", None)
    try:
        m = Migration.objects.get(username__iexact = f_username)
        user = {
            "username": m.username,
            "last_name": m.last_name,
            "first_name": m.first_name,
        }
    except Migration.DoesNotExist:
        user = None

    return JsonResponse(user, safe = False)


def get_member(request):
    f_username = request.POST.get("username", None)
    try:
        m = Member.objects.get(username__iexact = f_username)
        user = {
            "username": m.username,
            "last_name": m.last_name,
            "first_name": m.first_name,
        }
    except Member.DoesNotExist:
        user = None

    return JsonResponse(user, safe = False)


def validate_sponsor(request):
    form = request.POST.get("form", None)
    data = {}
    sponsor = ""

    if form is not None:
        form_data = str_to_json(form)

        f_sponsor = form_data['sponsor']
        sponsor = Member.objects.filter(username__exact = f_sponsor).first()
    else:
        data["form_error"] = _("No data submitted")

    if not sponsor:
        data["status"] = False
        data["messages"] = [_("This sponsor doesn't exist")]
    else:
        data["status"] = True
        data["messages"] = [sponsor.full_name]

    return JsonResponse(data)


def get_placement_name(request):
    form = request.POST.get("form", None)
    data = {}
    placement_name = ""
    placement_name_count = 0

    if form is not None:
        form_data = str_to_json(form)

        f_placement_name = form_data['placement_name']
        placement_name = Member.objects.filter(username__exact = f_placement_name).first()
        placement_name_count = Member.objects.filter(placement_name__exact = f_placement_name).count()
    else:
        data["form_error"] = _("No data submitted")

    if not placement_name:
        data["status"] = False
        data["messages"] = [_("This member doesn't exist")]
    else:
        data["status"] = True
        data["messages"] = [placement_name.full_name]
    if placement_name_count == 2:
        data["status"] = False
        data["messages"].append(_("This sponsor can no longer support people"))

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
    f_placement_name = request.POST.get("placement_name", None)
    f_placement_mode = request.POST.get("placement_mode", None)
    data = {}
    if f_placement_mode in ["left", "right"]:
        placement = Member.objects.filter(placement_name__exact = f_placement_name,
                                          placement_mode__exact = f_placement_mode).exists()

        if not placement:
            data["status"] = True
            data["messages"] = []
        else:
            data["status"] = False
            data["messages"] = [_("This sponsor can no longer add people under this side")]

        return JsonResponse(data)


def validate_email(request):
    f_email = request.POST.get("email", None)
    data = {}

    email_count = Member.objects.filter(email__exact = f_email).count()

    if email_count <= 2:
        data["status"] = True
        data["messages"] = []
    elif email_count == 3:
        data["status"] = False
        data["messages"] = [_("This email has reached the maximum number of subscription")]

    return JsonResponse(data)


def check_security_code(request):
    security_code = request.POST.get('security_code', None)
    data = {}
    member = request.user.member

    check = check_password_hash(member.security_code, security_code)

    if check:
        data["status"] = True
        data["messages"] = []
    else:
        data["status"] = False
        data["messages"] = [_("Wallet Password incorrect, please try again.")]

    return JsonResponse(data)


def check_balance(request):
    form = request.POST.get("form", None)
    payment_mode = request.POST.get('payment_mode', None)
    data = {}

    if form is not None:
        form_data = str_to_json(form)
        pack = form_data.get('pack', None)

        grade = Pack.objects.filter(id = int(pack)).first()
        if grade is not None:
            try:
                member_wallet = MemberWallet.objects.get(member__user = request.user)
                if payment_mode == "wallet1":
                    member_wallet = member_wallet.wallet1
                else:
                    member_wallet = member_wallet.wallet2

                if member_wallet >= grade.price:
                    data["status"] = "success"
                    data["message"] = _("You can process your order")
                else:
                    data["status"] = "warning"
                    data["message"] = _("Your Wallet balance is not sufficient to complete this order !!!")
            except MemberWallet.DoesNotExist as e:
                logger.warning(request, e)
                data["status"] = "warning"
                data["message"] = _("User's wallet don't exist")
        else:
            data["status"] = "error"
            data["message"] = _("No data submitted")

    return JsonResponse(data)
