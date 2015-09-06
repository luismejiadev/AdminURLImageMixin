# -*- coding: utf-8 -*-
from django import forms
from sorl.thumbnail.shortcuts import get_thumbnail
from django.utils.safestring import mark_safe
from django.db.models.fields import URLField
    
class AdminImageWidget(forms.URLInput):
    """
    An ImageField Widget for django.contrib.admin that shows a thumbnailed
    image as well as a link to the current one if it hase one.
    """

    def render(self, name, value, attrs=None):
        output = super(AdminImageWidget, self).render(name, value, attrs)
        
        if value:
            try:
                mini = get_thumbnail(value, 'x80', upscale=False)
                output = (
                             '<div style="float:left">'
                             '<a style="width:%spx;display:block;margin:0 0 10px" class="thumbnail" target="_blank" href="%s">'
                             '<img src="%s"></a>%s</div>'
                         ) % (mini.width, value, mini.url, output)
            except Exception:
                output = (
                             '<div style="float:left">'
                             '<span style="color:red;">El enlace no es una imagen</span>'
                             '</a>%s</div>'
                         ) % (output)                 
        return mark_safe(output)



class AdminURLImageMixin(object):
    """
    This is a mix-in for ModelAdmin subclasses to make ``ImageField`` show nicer
    form class and widget
    """
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, URLField):
            return db_field.formfield(widget=AdminImageWidget)
        sup = super(AdminURLImageMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)