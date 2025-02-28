from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Librarybranch

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    branch = forms.ModelChoiceField(
        queryset=Librarybranch.objects.all(),
        empty_label="Select a branch",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Preferred Branch"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'branch']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

from django import forms
from .models import Member, Librarybranch

class UpdateBranchForm(forms.ModelForm):
    branchid = forms.ModelChoiceField(
        queryset=Librarybranch.objects.all(),
        empty_label="Select a branch",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Preferred Branch"
    )

    class Meta:
        model = Member
        fields = ['branchid']
