is_required = {'class': 'required'}


class GalleryUploadForm(forms.Form):
    title_prefix = forms.CharField(max_length=75,
                                   widget=forms.TextInput(attrs=is_required),
                                   label=u'Photo title prefix')
    photographer = forms.CharField(max_length=100,
                                   widget=forms.TextInput(attrs=is_required),
                                   label=u'Photo title prefix')
    info = forms.CharField(max_length=100,
                           widget=forms.Textarea(attrs=is_required),
                           label=u'Extra information')
    tags = forms.CharField(max_length=255,
                           widget=forms.TextInput(attrs=is_required),
                           label=u'Tag photographs')

    def __init__(self, *args, **kwargs):
        gallery = kwargs.pop('gallery', '')
        super(ActivationForm, self).__init__(*args, **kwargs)
        self.fields['gallery'] = forms.CharField(max_length=50,
                                                 widget=forms.HiddenInput(attrs={'value': gallery}))
