from django import forms
from pets.models import Pet, Raca, Especie

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'foto',
            'nome',
            'raca',
            'data_nascimento',
            'peso',
            'sexo',
            'porte',
            'status'
        ]

        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do pet'}),
            'raca': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso em kg', 'step': '0.1'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'porte': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordena as raças pelo nome da espécie para agrupar visualmente
        self.fields['raca'].queryset = Raca.objects.select_related('especie').order_by('especie__nome', 'nome')

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and len(nome.strip()) < 2:
            raise forms.ValidationError('O nome do pet deve ter pelo menos 2 caracteres.')
        return nome 