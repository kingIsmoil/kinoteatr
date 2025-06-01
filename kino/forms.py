from django import forms
from .models import Review
from .models import PaymentMethod, UserCard

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['star_number', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'star_number': 'Оценка (1-5)',
            'description': 'Текст отзыва',
        }


class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=PaymentMethod.choices,
        widget=forms.RadioSelect,
        label='Способ оплаты'
    )
    card = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Выберите карту'
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = UserCard.objects.filter(user=user)
        if not self.fields['card'].queryset.exists():
            self.fields['card'].widget = forms.HiddenInput()