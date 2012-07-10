from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema

_ = MessageFactory('collective.ptg.galleria')

class IGalleriaDisplaySettings(IBaseSettings):
    galleria_theme = schema.Choice(
        title=_(u"galleria_theme_title", default=u"Theme"),
        default='light',
        vocabulary=SimpleVocabulary([
            SimpleTerm('dark', 'dark', _(u"label_dark", default=u"Dark")),
            SimpleTerm('light', 'light', _(u"label_light", default=u"Light")),
            SimpleTerm('classic', 'classic', _(u"label_classic",
                                               default=u"Classic"))
        ]))
    galleria_transition = schema.Choice(
        title=_(u"galleria_transition", default=u"Transition"),
        default='fadeslide',
        vocabulary=SimpleVocabulary([
            SimpleTerm('fadeslide', 'fadeslide', _(u"label_fadeslide",
                default=u"Fade Slide - fade between images and "
                        u"slide slightly at the same time")),
            SimpleTerm('fade', 'fade', _(u"label_fade",
                default=u"Fade - crossfade betweens images")),
            SimpleTerm('flash', 'flash', _(u"label_flash",
                default=u"Flash - fades into background color "
                        u"between images")),
            SimpleTerm('pulse', 'pulse', _(u"label_pulse",
                default=u"Pulse - quickly removes the image into background "
                        u"color, then fades the next image")),
            SimpleTerm('slide', 'slide', _(u"label_slide",
                default=u"Slide - slides the images depending on image "
                        u"position"))
        ]))
    galleria_auto_show_info = schema.Bool(
        title=_(u'galleria_label_auto_show_info', default="Auto show info"),
        description=_(u'galleria_desc_auto_show_info',
            default="start gallery out with info showing"),
        default=True)


class GalleriaDisplayType(BaseDisplayType):

    name = u"galleria"
    schema = IGalleriaDisplaySettings
    description = _(u"label_galleria_display_type",
        default=u"Galleria")

    js_theme_files = {
        'dark': '++resource++ptg.galleria/dark.js',
        'light': '++resource++ptg.galleria/light.js',
        'classic': '++resource++ptg.galleria/classic.js'
    }
    css_theme_files = {
        'dark': '++resource++ptg.galleria/dark.css',
        'light': '++resource++ptg.galleria/light.css',
        'classic': '++resource++ptg.galleria/classic.css'
    }

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(portal_url)s/%(css_file)s" />
<style>
#galleria{
    height: %(height)ipx;
}
</style>
""" % {
            'portal_url': self.portal_url,
            'height': self.height + 60,
            'css_file': self.css_theme_files[self.settings.galleria_theme]
        }

    def javascript(self):
        return u"""
<script type="text/javascript"
    src="%(portal_url)s/++resource++ptg.galleria/galleria.js"></script>
<script type="text/javascript"
    src="%(portal_url)s/%(js_file)s"></script>
<script type="text/javascript">
(function($){
$(document).ready(function() {
    // Initialize Galleria
    $('#galleria').galleria({
        theme: 'classic',
        transitionSpeed: %(duration)i,
        transition: "%(transition)s",
        autoplay: %(autoplay)s,
        clicknext: true,
        showInfo: %(showInfo)s
    });
});
})(jQuery);

</script>
""" % {
        'portal_url': self.portal_url,
        'js_file': self.js_theme_files[self.settings.galleria_theme],
        'duration': self.settings.duration,
        'transition': self.settings.galleria_transition,
        'autoplay': self.settings.timed and \
            str(self.settings.delay) or 'false',
        'showInfo': jsbool(self.settings.galleria_auto_show_info)
    }
GalleriaSettings = createSettingsFactory(GalleriaDisplayType.schema)