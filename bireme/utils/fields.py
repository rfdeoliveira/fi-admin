# -*- coding: utf-8 -*-

from django import forms

from django.utils.encoding import smart_text
from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.serializers.json import DjangoJSONEncoder
from utils.models import *

import json
import jsonfield

class JSONField(jsonfield.JSONField):
    """JSONField is a generic textfield that serializes/deserializes JSON objects"""

    def formfield(self, **kwargs):
        """Overwrite default formfield method to change html input to hidden and add custom css class"""
        defaults = {'widget': forms.HiddenInput(attrs={'class': "jsonfield"})}
        defaults.update(kwargs)

        return super(JSONField, self).formfield(**defaults)


class AuxiliaryChoiceField(models.Field):
    """ Custom model field that present in select widget the values of AuxCode table for the current field """

    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        """Overwrite  formfield to change html input to select and populate choiceis with auxiliar codes from database"""

        defaults = {'widget': forms.Select(), 'form_class': forms.ChoiceField,
                    'choices': BLANK_CHOICE_DASH + [(aux.code, aux) for aux in
                                                    AuxCode.objects.filter(field=self.name)]}

        defaults.update(kwargs)

        return super(AuxiliaryChoiceField, self).formfield(**defaults)


class MultipleAuxiliaryChoiceField(models.Field):
    """ Custom model field that present in select multiple widget the values of AuxCode table for the current field """

    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert JSON object to a string"""
        if self.null and value is None:
            return None
        return json.dumps(value)

    def formfield(self, **kwargs):
        """Overwrite  formfield to change html input to select  multiple and populate choiceis with auxiliar codes from database"""

        defaults = {'widget': forms.SelectMultiple(), 'form_class': forms.MultipleChoiceField,
                    'choices': BLANK_CHOICE_DASH + [(aux.code, aux) for aux in
                                                    AuxCode.objects.filter(field=self.name)]}

        defaults.update(kwargs)

        return super(MultipleAuxiliaryChoiceField, self).formfield(**defaults)