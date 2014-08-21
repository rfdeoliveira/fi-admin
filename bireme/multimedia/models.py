#! coding: utf-8
from django.utils.translation import ugettext_lazy as _, get_language
from django.db import models
from django.utils import timezone

from utils.models import Generic, Country
from main.choices import LANGUAGES_CHOICES

from django.contrib.contenttypes.generic import GenericRelation

# Media Type model
class MediaType(Generic):

    class Meta:
        verbose_name = _("Media type")
        verbose_name_plural = _("Media types")

    acronym = models.CharField(_("Acronym"), max_length=25, blank=True)
    language = models.CharField(_("Language"), max_length=10, choices=LANGUAGES_CHOICES)
    name = models.CharField(_("Name"), max_length=255)

    def get_translations(self):
        translation_list = ["%s^%s" % (self.language, self.name.strip())]
        translation = MediaTypeLocal.objects.filter(media_type=self.id)
        if translation:
            other_languages = ["%s^%s" % (trans.language, trans.name.strip()) for trans in translation]
            translation_list.extend(other_languages)
        
        return translation_list

    def __unicode__(self):
        lang_code = get_language()
        translation = MediaTypeLocal.objects.filter(media_type=self.id, language=lang_code)
        if translation:
            return translation[0].name
        else:
            return self.name


class MediaTypeLocal(models.Model):

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    media_type = models.ForeignKey(MediaType, verbose_name=_("Media type"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES)
    name = models.CharField(_("name"), max_length=255)


# Collection model
class Collection(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(_("Description"), blank=False)

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")        

    def __unicode__(self):
        return self.name


class CollectionLocal(models.Model):

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    media_type = models.ForeignKey(Collection, verbose_name=_("Collection"))
    language = models.CharField(_("language"), max_length=10, choices=LANGUAGES_CHOICES)
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("Description"), blank=False)


# Media model
class Media(Generic):

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medias")

    STATUS_CHOICES = (
        (0, _('Pending')),
        (1, _('Admitted')),
        (2, _('Refused')),
        (3, _('Deleted')),
    )

    status = models.SmallIntegerField(_('Status'), choices=STATUS_CHOICES, null=True, default=0)
    media_type = models.ForeignKey(MediaType, verbose_name=_("Media type"), blank=False)
    title = models.CharField(_('Title'), max_length=455, blank=False)
    url = models.URLField(_('URL'), blank=False)
    author = models.TextField(_('Authors'), blank=True, help_text=_("Enter one per line"))
    description = models.TextField(_("Description"), blank=True)

    # responsible cooperative center
    cooperative_center_code = models.CharField(_('Cooperative center'), max_length=55, blank=True)

    def __unicode__(self):
        return self.title
