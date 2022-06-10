from django import forms

from .models import Products, Group


class ProductForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'groups__checkbox'}),
        to_field_name='slug',
        required=False
    )

    class Meta:
        model = Products
        fields = ('name', 'price', 'groups',
                  'description', 'image',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input'}),
            'price': forms.NumberInput(
                attrs={'class': 'form__input',
                       'id': 'id_price',
                       'name': 'price'}),
            'description': forms.Textarea(attrs={'class': 'form__textarea',
                                                 'rows': '8'}),
            'groups': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'image': 'Загрузить фото'
        }
