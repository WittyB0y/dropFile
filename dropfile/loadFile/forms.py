from django import forms
from loadFile.models import files, FileAccess, renderData


class AddUserAccess(forms.ModelForm):
    fileid = forms.ModelChoiceField(queryset=files.objects.none(), label='Выбери файл, которым будешь делиться:')
    existBefore = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Доступ открыт до:'
    )
    lookingSeeUsers = forms.CharField(label='Имя пользователя')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('userid')
        super().__init__(*args, **kwargs)
        self.fields['fileid'].queryset = files.objects.filter(userid=user)

    class Meta:
        model = FileAccess
        fields = ('fileid', 'existBefore', 'lookingSeeUsers')


class UserAccess(forms.ModelForm):
    # TODO .none()
    # fileLink = forms.ModelChoiceField(queryset=renderData.objects.all(), label='Выбери файл, которым будешь делиться:')

    class Meta:
        model = renderData
        fields = '__all__'
