from django import forms

from .models import Products, Groups


class ProductForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(
        queryset=Groups.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'group__checkbox'}),
        to_field_name='slug',
        required=False
    )

    class Meta:
        model = Products
        fields = ('name', 'price', 'group',
                  'description', 'image',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input'}),
            'price': forms.NumberInput(
                attrs={'class': 'form__input',
                       'id': 'id_price',
                       'name': 'price'}),
            'description': forms.Textarea(attrs={'class': 'form__textarea',
                                                 'rows': '8'}),
            'group': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'image': 'Загрузить фото'
        }
