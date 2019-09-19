from crispy_forms.helper import FormHelper
from django import forms

from .models import MainWallet, MemberWallet


class AddBalanceForm(forms.ModelForm):
    class Meta:
        model = MainWallet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddBalanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'


class MemberWalletForm(forms.ModelForm):
    class Meta:
        model = MemberWallet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemberWalletForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4 col-sm-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-sm-8 col-md-8 col-lg-8'
