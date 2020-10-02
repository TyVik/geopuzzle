from django import forms
from django.db import models
from django.utils.safestring import SafeText


class ExternalIdWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None) -> SafeText:
        result = super().render(name, value, attrs, renderer)
        if value is not None:
            result += ' <a href="{link}" target="_blank" rel="noopener noreferrer">link</a>'.\
                format(link=self.attrs['link']).\
                format(id=value)
        return result


class ExternalIdFormField(forms.CharField):
    def __init__(self, *args, link='', **kwargs):
        self.link = link
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        result = super().widget_attrs(widget)
        result.update({'link': self.link})
        return result


class ExternalIdField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.link = kwargs.pop('link', '')
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = kwargs
        # (link='https://www.wikidata.org/wiki/{id}')
        defaults.update({'form_class': ExternalIdFormField, 'widget': ExternalIdWidget, 'link': self.link})
        return super().formfield(**defaults)


class RegionsField(models.ManyToManyField):
    def save_form_data(self, instance, data):
        self.remote_field.through.objects.filter(puzzle=instance).delete()
        self.remote_field.through.objects.bulk_create([
            self.remote_field.through(puzzle=instance, region=region)
            for region in data])
