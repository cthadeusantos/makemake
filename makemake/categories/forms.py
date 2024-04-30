from django import forms
from django.forms import ModelChoiceField, formset_factory, inlineformset_factory
from makemake.categories.models import Category
from makemake.documents.models import Document


class CategoryForm(forms.Form):
    code = forms.CharField(label='Code',
                           widget=forms.Textarea(attrs={'name': 'code',
                                                        'rows': 1,
                                                        'cols': 3,
                                                        'style': 'resize:none',
                                                        'class': 'form-control form-control-sm text-uppercase',
                                                        'maxlenght': 3,
                                                        'size': 3,
                                                        }),
                                                        )
    name = forms.CharField(label='Name',
                               widget=forms.Textarea(attrs={'name': 'name','rows': 1,
                                                            'cols': 50,
                                                            'style': 'resize:none',
                                                            'class': 'form-control form-control-sm',
                                                            'maxlenght': 50,
                                                            }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 2,
                                                               'cols': 50,
                                                               'style': 'resize:none',
                                                               'class': 'form-control form-control-sm',
                                                               }))
    category = ModelChoiceField(label='Parent category',
                                queryset=Category.objects.filter(category=None),
                                required=False,
                                widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))

    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        if prefix == 'edit':
            self.fields['code'].initial = instance.code
            self.fields['name'].initial = instance.name
            self.fields['description'].initial = instance.description
            self.fields['code'].widget.attrs['readonly'] = True
            self.fields['category'].queryset = Category.objects.filter(category=None).exclude(pk=instance.pk).order_by('name')
            self.fields['category'].initial = instance.category

