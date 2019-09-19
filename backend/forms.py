from crispy_forms.helper import FormHelper
from django import forms
from django.forms import inlineformset_factory

from .models import Member, BankInfo, OrderInfo, MaintenancePack


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'security_code': forms.PasswordInput(),
        }
        exclude = ('user', 'security_code', 'status',)

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'


class SecurityCodeForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('security_code',)
        widgets = {
            'security_code': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(SecurityCodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'


class BankInfoForm(forms.ModelForm):
    class Meta:
        model = BankInfo
        fields = '__all__'
        exclude = ('member',)

    def __init__(self, *args, **kwargs):
        super(BankInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'


class OrderInfoForm(forms.ModelForm):
    class Meta:
        model = OrderInfo
        fields = '__all__'
        exclude = ('member',)

    def __init__(self, *args, **kwargs):
        super(OrderInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'


class MaintenancePackForm(forms.ModelForm):
    class Meta:
        model = MaintenancePack
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MaintenancePackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'


OrderInfoFormSet = inlineformset_factory(Member, OrderInfo, form = OrderInfoForm, fields = "__all__",
                                         can_delete = False)
