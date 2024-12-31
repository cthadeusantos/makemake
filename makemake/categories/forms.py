from django import forms
from django.forms import ModelChoiceField, formset_factory, inlineformset_factory
from makemake.categories.models import Category
from makemake.documents.models import Document
from makemake.core.tailwind_classes import *

class CategoryForm(forms.Form):
    code = forms.CharField(label='Code',
                           widget=forms.Textarea(attrs={'name': 'code',
                                                        'rows': 1,
                                                        'cols': 3,
                                                        'style': 'resize:none',
                                                        'class': CSS_CHARFIELD_1,
                                                        }),
                                                        max_length=3,
                                                        )
    name = forms.CharField(label='Name',
                               widget=forms.Textarea(attrs={'name': 'name','rows': 1,
                                                            'cols': 50,
                                                            'style': 'resize:none',
                                                            'class': CSS_CHARFIELD_1,
                                                            }),
                                                            max_length=50,
                                                            )
    description = forms.CharField(label='Description',
                                  required=False,
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 2,
                                                               'cols': 50,
                                                               'style': 'resize:none',
                                                               'class': CSS_TEXTFIELD_1,
                                                               }))

    fordocs = forms.BooleanField(required=False, label='Used in documents', widget=forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-blue-600'}))
    forbudgets = forms.BooleanField(required=False, label='Used in budgets', widget=forms.CheckboxInput(attrs={'class': 'form-checkbox h-4 w-4 text-blue-600'}))

    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        
        if prefix == 'edit':
            self.fields['code'].initial = instance.code
            self.fields['name'].initial = instance.name
            self.fields['description'].initial = instance.description
            self.fields['code'].widget.attrs['readonly'] = True
            self.fields['fordocs'].initial = instance.fordocs
            self.fields['forbudgets'].initial = instance.forbudgets
        else:
            self.fields['fordocs'].initial = True

    def clean_code(self):
        code = self.cleaned_data['code'].upper()
        if not code.isalpha():
            raise forms.ValidationError("Please enter only letters.")
        # try:
        #     category = Category.objects.get(code=code)
        #     raise forms.ValidationError("Code category must be unique!")
        # except Category.DoesNotExist:
        #     pass  # Nenhum objeto encontrado com esse código, então tudo certo
        return code
    
class ParentsForm(forms.Form):
    parent = forms.ModelChoiceField(#label='Parent category',
                            queryset=Category.objects.filter(parents=None),
                            required=False,
                            widget=forms.Select(attrs={
                                'class': CSS_SELECT_1,
                                                       }),
                                                       )
        
    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(ParentsForm, self).__init__(*args, **kwargs)
        
        # Modificar o name do campo 'parent' dinamicamente
        # if prefix == 'edit':
            #self.fields['parent'].queryset = Category.objects.filter(parents=None).exclude(pk=instance.pk).order_by('name')
            # self.fields['parent'].queryset = Category.objects.all().exclude(pk__in=Category.objects.filter(pk=instance.pk).values_list('id'))
            # self.fields['parent'].initial = instance.parents

# Crie um formset manualmente para o BookForm
CategoryFormSet = formset_factory(ParentsForm, extra=1,)  # `extra` define o número de formulários extras exibidos
