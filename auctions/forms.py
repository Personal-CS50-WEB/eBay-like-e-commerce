from django import forms
from .models import Category

class NewListingForm(forms.Form):
    ''' form for new listing'''
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
                                    'placeholder': 'Title', 'class':'form-control'
                                }))
    
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={
                                        'placeholder': 'Write description','class':'form-control'
                                    }))
    image = forms.URLField(label='Add image', required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    start_bid = forms.DecimalField(label='Start bid',max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={
                                        'class': 'form-control'
                                    }))
    category = forms.ChoiceField(label='Category', choices=Category.objects.values_list(), widget=forms.Select(attrs={
                                        'class':'form-control'
                                    }))


class BidForm(forms.Form):
    bid = forms.DecimalField(label="",max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={
                                        'placeholder': 'Your bid',
                                        'class': 'form-control'
                                    }))


class CommentForm(forms.Form):
    comment =  forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control'}))
