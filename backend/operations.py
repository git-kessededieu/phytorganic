from django.contrib.auth.models import User

from backend.bonus import teeps_handler, sponsorship_bonus_handler, team_bonus_handler, activation_bonus_handler
from backend.methods import generate_password, member_status_update, set_counter
from backend.models import Pack, Member, Counter
from backend.transactions import order_tnx_handler
from frontend.enums import GRADES, UPGRADE_DAYS
from phytorganic.notify import notifier
from wallet.transactions import operation_tnx


def member_creation(data):
    parent = Member.objects.filter(username = data['placement_name']).first()
    password = generate_password()
    member_info = {
        'username': data.get('username', ''),
        'first_name': data.get('first_name', ''),
        'last_name': data.get('last_name', ''),
        'email': data.get('email', ''),
        'sponsor': data.get('sponsor', ''),
        'parent': parent,
        'placement_name': data.get('placement_name', ''),
        'placement_mode': data.get('placement_mode', ''),
        'grade': data.get('grade', ''),
        'contact': data.get('contact', ''),
        'security_code': password
    }
    member = Member(**member_info)
    member.save()
    return member


def member_registration(request, data):
    placement_name = data.get('placement_name', None)
    pack = data.get('pack', None)
    delivery_method = data.get('delivery_method', None)
    payment_mode = data.get('payment_mode', None)
    pack = Pack.objects.filter(id = int(pack)).first()

    """1. MEMBER CREATION"""
    parent = Member.objects.filter(username = placement_name).first()
    password = generate_password()
    member_info = {
        'username': data.get('username', None),
        'first_name': data.get('first_name', None),
        'last_name': data.get('last_name', None),
        'email': data.get('email', None),
        'sponsor': data.get('sponsor', None),
        'parent': parent,
        'placement_name': data.get('placement_name', None),
        'placement_mode': data.get('placement_mode', None),
        'grade': "" if pack is None else pack.code,
        'paper_id': data.get('paper_id', None),
        'gender': data.get('gender', None),
        'birth_date': data.get('birth_date', None),
        'contact': data.get('contact', None),
        'residential_country': data.get('residential_country', None),
        'address_1': data.get('address_1', None),
        'address_2': data.get('address_2', None),
        'post_code': data.get('post_code', None),
        'city': data.get('city', None),
        'state': data.get('state', None),
        'country': data.get('country', None),
        'security_code': password
    }
    member = Member(**member_info)
    print("Member => {}".format(member))
    member.save()

    """2. ORDER PROCESS"""
    sender = request.user.member
    print("Enroller => {}".format(sender))

    operation_data = {
        'member': sender,
        'wallet': payment_mode,
        'sender': sender,
        'receiver': member,
        'operation': 'registration',
        'created_by': sender
    }
    operation_status = operation_tnx("m2M", pack.price, **operation_data)

    print("Operation Data => {}".format(operation_data))
    print("Operation Status => {}".format(operation_status))

    if operation_status:
        """3. UPDATE MEMBER STATUS"""
        member_status_update(member, True)

        """4. ORDER INFO"""
        order_tnx_handler(member = member, order_type = "P", pack = pack, payment_mode = payment_mode,
                          delivery_method = delivery_method)

        """5. TEEPS"""
        teeps_handler(request, pack = pack)

        """6. SPONSORSHIP BONUS"""
        sponsorship_bonus_handler(request, sponsor = member.sponsor, pack = pack)

        """7. TEAM BONUS"""
        team_bonus_handler(request, pack = pack, member = member, operation = "team_bonus")

        notify_data = {
            'action': 'registration',
            'e_subject': 'PhytOrganic - Member Registration',
            'e_receiver': member.email,
            'e_context': {'username': member.username, 'password': password}
        }
        notifier(**notify_data)
        return True
    else:
        return False


def member_activation(request, data):
    sender = data.get('sender')
    receiver = data.get('receiver')
    amount = data.get('amount')

    operation_data = {
        'member': sender,
        'wallet': "wallet2",
        'sender': sender,
        'receiver': receiver,
        'operation': 'activation',
        'created_by': sender
    }
    operation_status = operation_tnx("m2M", amount, **operation_data)

    print("Operation Data => {}".format(operation_data))
    print("Operation Status => {}".format(operation_status))
    activation_bonus_handler(request, **{'member': receiver, 'operation': 'activation'})

    if operation_status:
        member_status_update(receiver, True)

        """Autoship Counter Init"""
        autoship = Counter.objects.get(code = "autoship")
        set_counter(receiver, autoship)

        print("Member Grade => {}".format(receiver.grade))
        print("ENUMS GRADE => {}".format(GRADES.diamond))

        if receiver.grade == GRADES.diamond:
            """Pool 10 Counter Init"""
            pool_10 = Counter.objects.get(code = "pool_10")
            set_counter(receiver, pool_10)
        else:
            """Upgrade Counter Init"""
            upgrade = Counter.objects.get(code = "upgrade")
            set_counter(receiver, upgrade)

        password = generate_password()

        user = User.objects.get(username = receiver.username)
        user.set_password(password)
        user.save()

        notify_data = {
            'action': 'activation',
            'e_subject': 'PhytOrganic - Member Activation',
            'e_receiver': receiver.email,
            'e_context': {'username': receiver.username, 'password': password}
        }
        notifier(**notify_data)
        return True
