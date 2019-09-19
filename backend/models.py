import calendar
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django_countries.fields import CountryField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from backend.managers import MemberManager
from frontend.enums import GENDER, GRADES, PLACEMENT_MODE, COUNTRIES, DELIVERY, PAYMENT_MODE, BV_SIDE
from frontend.models import Product


def get_pack_price(order_type, pack):
    if order_type == "P":
        return Pack.objects.get(id = pack).price
    elif order_type == "MP":
        return MaintenancePack.objects.get(id = pack).price


def get_month_day_range(date):
    """
    For a date 'date' returns the start and end date for the month of 'date'.

    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day


class Leadership(models.Model):
    id = models.BigAutoField(primary_key = True)
    title = models.CharField(max_length = 160, verbose_name = _("Title"))
    code = models.CharField(max_length = 60, verbose_name = _("Pack"), editable = False)

    def save(self, *args, **kwargs):
        letters = [word[0] for word in self.title.split()]
        if self.code != letters:
            self.code = "".join(letters)
        super(Leadership, self).save(*args, **kwargs)

    class Meta:
        db_table = 'leadership'
        verbose_name = 'Leadership'
        verbose_name_plural = 'Leaderships'

    def __str__(self):
        return "{}".format(self.title)


class Member(MPTTModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE, default = None, null = True, editable = False,
                                related_name = 'member')
    last_name = models.CharField(max_length = 60, verbose_name = _("Last Name"))
    first_name = models.CharField(max_length = 255, verbose_name = _("First Name"))
    username = models.CharField(max_length = 60, unique = True, verbose_name = _("Username"))
    email = models.EmailField(verbose_name = _("Email"))
    contact = models.CharField(max_length = 60, verbose_name = _("Contact"))
    paper_id = models.CharField(max_length = 255, default = "", blank = True, verbose_name = _("I.D. Card/Passport."))
    sponsor = models.CharField(max_length = 60, default = "", blank = True, verbose_name = _("Sponsor"))
    parent = TreeForeignKey('self', on_delete = models.CASCADE, blank = True, null = True, related_name = 'children',
                            verbose_name = _("Member Placement"))
    # level = models.PositiveIntegerField(default = 0, verbose_name = _("Level"))
    placement_name = models.CharField(max_length = 60, default = "", blank = True, verbose_name = _("Placement Name"))
    grade = models.CharField(max_length = 10, choices = GRADES, verbose_name = _("Grade"))
    leadership = models.ForeignKey(Leadership, on_delete = models.SET_NULL, blank = True, null = True,
                                   verbose_name = _("Leadership"))
    placement_mode = models.CharField(max_length = 10, choices = PLACEMENT_MODE, default = "", blank = True,
                                      verbose_name = _("Placement Mode"))
    residential_country = CountryField(default = "", blank = True, verbose_name = _("Residential Country"))
    mobile = models.CharField(max_length = 60, default = "", blank = True, verbose_name = _("Mobile Phone"))
    birth_date = models.DateField(null = True, blank = True, verbose_name = _("Birth Date"))
    gender = models.CharField(max_length = 10, default = "", blank = True, choices = GENDER, verbose_name = _("Gender"))
    address_1 = models.CharField(max_length = 255, default = "", blank = True, verbose_name = _("Address Line 1"))
    address_2 = models.CharField(max_length = 255, default = "", blank = True, verbose_name = _("Address Line 2"))
    post_code = models.CharField(max_length = 10, default = "", blank = True, verbose_name = _("Post Code"))
    country = models.CharField(max_length = 160, choices = COUNTRIES, default = "", blank = True,
                               verbose_name = _("Country"))
    city = models.CharField(max_length = 60, default = "", blank = True, verbose_name = _("City"))
    state = models.CharField(max_length = 60, default = "", blank = True, verbose_name = _("State"))
    photo = models.ImageField(upload_to = 'images/members/', default = None, blank = True, null = True)
    security_code = models.CharField(max_length = 255, default = "", blank = True, verbose_name = _("Security Code"))
    message = models.TextField(default = "", blank = True, verbose_name = _("Message"))
    status = models.BooleanField(default = False, verbose_name = "Account Status")
    created_at = models.DateTimeField(auto_now_add = True, editable = False)
    updated_at = models.DateTimeField(auto_now = True, editable = False)
    objects = models.Manager()
    genealogy = MemberManager()

    class Meta:
        db_table = 'member'
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    class MPTTMeta:
        order_insertion_by = ['username']

    def __str__(self):
        return "{0} - {1} {2}".format(self.username, self.first_name, self.last_name)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @staticmethod
    def get_absolute_url():
        return reverse('backend:profile')


class BankInfo(models.Model):
    member = models.OneToOneField(Member, models.CASCADE, verbose_name = _("Member"))
    branch = models.CharField(max_length = 160, default = "", blank = True, verbose_name = _("Bank Branch"))
    swift = models.CharField(max_length = 160, default = "", blank = True, verbose_name = _("Swift Code"))
    account_number = models.CharField(max_length = 160, default = "", blank = True, verbose_name = _("Bank Account N°"))

    class Meta:
        db_table = 'bank_info'
        verbose_name = 'Bank Info'
        verbose_name_plural = 'Bank Infos'

    def __str__(self):
        return "{}".format(self.member)


class MemberBV(models.Model):
    member = models.OneToOneField(Member, models.CASCADE, related_name = "member_bv", verbose_name = _("BV Owner"))
    left = models.PositiveIntegerField(default = 0, verbose_name = _("Business Volume Left"))
    right = models.PositiveIntegerField(default = 0, verbose_name = _("Business Volume Right"))

    class Meta:
        db_table = 'member_bv'
        verbose_name = 'Member Business Volume'
        verbose_name_plural = 'Member Business Volumes'

    def __str__(self):
        return "{0} : {1} - {2}".format(self.member, self.left, self.right)


class Pack(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 60, verbose_name = _("Pack"))
    code = models.CharField(max_length = 60, verbose_name = _("Pack"), editable = False)
    price = models.DecimalField(max_digits = 20, decimal_places = 2, default = 250, verbose_name = _("Price"))
    bv = models.PositiveIntegerField(default = 100, verbose_name = _("Business Volume"))
    level = models.PositiveSmallIntegerField(default = 0, verbose_name = _("Matrix Level"))
    qty = models.PositiveIntegerField(default = 4, verbose_name = _("Products Number"))
    autoship_time = models.PositiveIntegerField(default = 100, verbose_name = _("Time for Auto Ship"),
                                                help_text = "In Days")
    upgrade_time = models.PositiveIntegerField(default = 60, verbose_name = _("Time for upgrade"),
                                               help_text = "In Days")
    upgrade_bv = models.PositiveIntegerField(default = 400, verbose_name = _("BV for upgrade"))

    class Meta:
        db_table = 'pack'
        verbose_name = 'Pack'
        verbose_name_plural = 'Packs'

    def __str__(self):
        return "{0} (${1}, {2} BV)".format(self.name, self.price, self.bv)

    def save(self, *args, **kwargs):
        code = self.name.lower().replace(' ', '_')
        if self.code != code:
            self.code = code
        super(Pack, self).save(*args, **kwargs)


class MaintenancePack(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 60, verbose_name = _("Pack"))
    code = models.CharField(max_length = 60, verbose_name = _("Pack"), editable = False)
    price = models.DecimalField(max_digits = 20, decimal_places = 2, default = 100, verbose_name = _("Price"))
    bv = models.PositiveIntegerField(default = 25, verbose_name = _("Business Volume"))
    qty = models.PositiveIntegerField(default = 2, verbose_name = _("Products Number"))

    class Meta:
        db_table = 'maintenance_pack'
        verbose_name = 'Maintenance Pack'
        verbose_name_plural = 'Maintenance Packs'

    def __str__(self):
        return "{0} (${1}, {2} BV)".format(self.name, self.price, self.bv)

    def save(self, *args, **kwargs):
        code = self.name.lower().replace(' ', '_')
        if self.code != code:
            self.code = code
        super(MaintenancePack, self).save(*args, **kwargs)


class Grade(models.Model):
    id = models.AutoField(primary_key = True)
    start_grade = models.ForeignKey(Pack, on_delete = models.SET_NULL, blank = True, null = True,
                                    related_name = "start_grade", verbose_name = _("Start Pack"))
    end_grade = models.ForeignKey(Pack, on_delete = models.SET_NULL, blank = True, null = True,
                                  related_name = "end_grade", verbose_name = _("end Pack"))
    bv = models.PositiveIntegerField(default = 400, verbose_name = _("Personal Business Volume"))
    days = models.PositiveIntegerField(default = 60, verbose_name = _("Days"))

    class Meta:
        db_table = 'grade'
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return "{0} => {1}, {2} BV".format(self.start_grade, self.end_grade, self.bv)


class OrderInfo(models.Model):
    ORDER_TYPE = (
        ('MP', 'MaintenancePack'),
        ('P', 'Pack'),
    )

    id = models.BigAutoField(primary_key = True)
    member = models.ForeignKey(Member, models.CASCADE, related_name = "orders", verbose_name = _("Member"))
    order_type = models.CharField(max_length = 3, choices = ORDER_TYPE, verbose_name = _("Order Type"))
    pack = models.IntegerField(blank = True, null = True, verbose_name = _("Pack"))
    price = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0, verbose_name = _("Price"))
    payment_mode = models.CharField(max_length = 15, choices = PAYMENT_MODE, default = PAYMENT_MODE.wallet2,
                                    blank = True, verbose_name = _("Payment Mode"))
    delivery_method = models.CharField(max_length = 15, choices = DELIVERY, blank = True,
                                       verbose_name = _("Delivery Method"))
    order_date = models.DateTimeField(auto_now_add = True, editable = False)

    class Meta:
        db_table = 'order_info'
        verbose_name = 'Order Info'
        verbose_name_plural = 'Order Infos'

    def __str__(self):
        return "{}".format(self.member)

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = get_pack_price(self.order_type, self.pack)
        super(OrderInfo, self).save(*args, **kwargs)


class OperationType(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 255, verbose_name = _("Operation"))
    code_name = models.CharField(max_length = 100, editable = False, verbose_name = _("Code Name"))

    class Meta:
        db_table = 'operation_type'
        verbose_name = 'Operation Type'
        verbose_name_plural = 'Operation Types'

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        code_name = self.name.lower().replace(' ', '_')
        if self.code_name != code_name:
            self.code_name = code_name
        super(OperationType, self).save(*args, **kwargs)


class MemberBVHistory(models.Model):
    id = models.BigAutoField(primary_key = True)
    member = models.ForeignKey(Member, models.CASCADE, related_name = "m_receiver", editable = False,
                               verbose_name = _("Member"))
    bv = models.IntegerField(default = 0, editable = False, verbose_name = _("Business Volume"))
    side = models.CharField(max_length = 10, choices = BV_SIDE, editable = False, verbose_name = "Side")
    origin = models.ForeignKey(OperationType, on_delete = models.SET_NULL, blank = True, null = True, editable = False,
                               verbose_name = _("Origin"))
    sender = models.ForeignKey(Member, models.CASCADE, related_name = "m_sender", blank = True, null = True,
                               editable = False, verbose_name = _("Sender"))
    tnx_date = models.DateTimeField(auto_now_add = True, editable = False)

    class Meta:
        db_table = 'member_bv_history'
        verbose_name = 'Business Volume History'
        verbose_name_plural = 'Business Volume History'

    def __str__(self):
        return "{0} - {1} : {2}".format(self.tnx_date.date(), self.member, self.bv)


class Counter(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 60, verbose_name = _("Counter Name"))
    description = models.TextField(default = "", blank = True, verbose_name = _("Counter Description"))
    code = models.CharField(max_length = 60, verbose_name = _("Code"), editable = False)

    class Meta:
        db_table = 'counter'
        verbose_name = 'Counter'
        verbose_name_plural = 'Counters'

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        code = self.name.lower().replace(' ', '_')
        if self.code != code:
            self.code = code
        super(Counter, self).save(*args, **kwargs)


class MemberCounter(models.Model):
    member = models.ForeignKey(Member, models.CASCADE, related_name = "member_counter", verbose_name = _("Member"))
    counter = models.ForeignKey(Counter, models.CASCADE, verbose_name = _("Counter"))
    # days = models.IntegerField(default = 0, verbose_name = _("Days"), help_text = "In Days")
    state = models.BooleanField(default = True, verbose_name = _("Counter State"))
    start_date = models.DateTimeField(default = timezone.now, editable = False, verbose_name = _("Start Date"))
    end_date = models.DateTimeField(default = timezone.now, editable = False, verbose_name = _("End Date"))

    class Meta:
        db_table = 'member_counter'
        verbose_name = 'Member Counter'
        verbose_name_plural = 'Member Counters'

    def __str__(self):
        return "{0} {1}".format(self.member, self.counter)

    def save(self, *args, **kwargs):
        pack = Pack.objects.get(code = self.member.grade)
        if self.counter.code == "autoship":
            self.end_date = self.start_date + timedelta(days = pack.autoship_time)
        if self.counter.code == "upgrade":
            self.end_date = self.start_date + timedelta(days = pack.upgrade_time)
        if self.counter.code == "pool_10":
            self.end_date = get_month_day_range(self.start_date)[1]
            # self.end_date = self.start_date + timedelta(days = pack.upgrade_time)
        super(MemberCounter, self).save(*args, **kwargs)


class LeadershipConditions(models.Model):
    id = models.BigAutoField(primary_key = True)
    member = models.ForeignKey(Member, models.CASCADE, related_name = "member", verbose_name = _("Member"))
    leadership = models.ForeignKey(Leadership, models.CASCADE, verbose_name = _("Leadership Status"))
    team = models.ForeignKey(Member, models.CASCADE, related_name = "team", verbose_name = _("Team"))
    personal_volume = models.DecimalField(max_digits = 20, decimal_places = 2, default = 1500,
                                          verbose_name = _("Personal Volume"))
    bv = models.PositiveIntegerField(default = 500, verbose_name = _("Business Volume"))

    class Meta:
        db_table = 'leadership_conditions'
        verbose_name = 'Leadership Condition'
        verbose_name_plural = 'Leaderships Conditions'

    def __str__(self):
        return "{0} => {1}".format(self.member, self.leadership)
