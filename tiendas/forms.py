from django import forms


class CheckoutForm(forms.Form):
    nombre = forms.CharField(max_length=120, label='Nombre')
    telefono = forms.CharField(max_length=30, label='Teléfono')
    direccion = forms.CharField(widget=forms.Textarea, label='Dirección')
    metodo_pago = forms.ChoiceField(
        choices=[('transferencia', 'Transferencia'), ('efectivo', 'Efectivo')],
        label='Método de pago'
    )