from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema
from plone.memoize.view import memoize

_ = MessageFactory('collective.ptg.galleria')

class IGalleriaDisplaySettings(IBaseSettings):
    galleria_theme = schema.Choice(
        title=_(u"galleria_theme_title", default=u"Theme"),
        default='light',
        vocabulary=SimpleVocabulary([
            SimpleTerm('dark', 'dark', _(u"label_dark", default=u"Dark")),
            SimpleTerm('light', 'light', _(u"label_light", default=u"Light")),
            SimpleTerm('fullscreen', 'fullscreen', _(u"label_fullscreen", default=u"Fullscreen")),
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
    galleria_height = schema.Int(
        title=_(u'galleria_label_galleria_height', default="Height of gallery"),
        description=_(u'galleria_galleria_height',
            default="Height in pixels"),
        default=300) 
    galleria_imagenav = schema.Bool(
        title=_(u'galleria_label_imagenav', default="Enable Imagenav"),
        description=_(u'galleria_imagenav',
            default="enable the next and previous button"),
        default=True) 
    galleria_thumbnails = schema.Bool(
        title=_(u'galleria_label_thumbnails', default="Enable Thumbnails"),
        description=_(u'galleria_thumbnails',
            default="enable the thumbnails at bottom"),
        default=True)      
    galleria_lightbox = schema.Bool(
        title=_(u'galleria_label_lightbox', default="Enable lightbox"),
        description=_(u'galleria_lightbox',
            default="enable lightbox when clicking on main image"),
        default=False)
    galleria_carousel = schema.Bool(
        title=_(u'galleria_carousel', default="Enable carousel"),
        description=_(u'galleria_carousel',
            default="enable carousel for thumbnails (you want this ON)"),
        default=True)  
    galleria_carousel_steps = schema.Int(
        title=_(u'galleria_carousel_steps', default="Carousel steps"),
        description=_(u'Carousel steps',
            default="Defines how many 'steps' the carousel should take on each nav click."),
        default=1)  
    galleria_responsive = schema.Bool(
        title=_(u'galleria_responsive', default="Resposive mode"),
        description=_(u'galleria_responsive',
            default="this setting is only useful if your theme is responsive"),
        default=False)    
    galleria_history = schema.Bool(
        title=_(u'galleria_history', default="Enable history plugin"),
        description=_(u'galleria_history',
            default="Enables the browsers back button"),
        default=False)
    galleria_include_download_link = schema.Bool(
        title=_(u'galleria_download_url', default=u"Show download link"),
        default=False)


class GalleriaDisplayType(BaseDisplayType):

    name = u"galleria"
    schema = IGalleriaDisplaySettings
    description = _(u"label_galleria_display_type",
        default=u"Galleria")

    js_theme_files = {
        'dark': '++resource++ptg.galleria/dark.js',
        'light': '++resource++ptg.galleria/light.js',
        'classic': '++resource++ptg.galleria/classic.js',
        'fullscreen': '++resource++ptg.galleria/fullscreen.js'
    }
    css_theme_files = {
        'dark': '++resource++ptg.galleria/dark.css',
        'light': '++resource++ptg.galleria/light.css',
        'classic': '++resource++ptg.galleria/classic.css',
        'fullscreen': '++resource++ptg.galleria/fullscreen.css'
    }

    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(portal_url)s/%(css_file)s" />
""" % {
            'portal_url': self.portal_url,
            'height': self.settings.galleria_height + 60,
            'css_file': self.css_theme_files[self.settings.galleria_theme],
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
        transitionSpeed: %(duration)i,
        transition: "%(transition)s",
        autoplay: %(autoplay)s,
        clicknext: true,
        showInfo: %(showInfo)s,
        lightbox: %(lightbox)s,
        carousel: %(carousel)s,
        responsive: %(responsive)s,
        carouselSteps: %(carousel_steps)s,
        trueFullscreen: true,
        thumbnails: %(thumbnails)s,
        showImagenav: %(imagenav)s,
        height: %(height)i
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
        'showInfo': jsbool(self.settings.galleria_auto_show_info),
        'lightbox': jsbool(self.settings.galleria_lightbox),
        'carousel': jsbool(self.settings.galleria_carousel),
        'responsive': jsbool(self.settings.galleria_responsive),
        'carousel_steps': self.settings.galleria_carousel_steps,
        'imagenav': jsbool(self.settings.galleria_imagenav),
        'thumbnails': jsbool(self.settings.galleria_thumbnails),
        'height': self.settings.galleria_height
    }

    @property
    @memoize
    def include_download_url(self):
        return self.settings.galleria_include_download_link

    def format_description(self, img):
        if not self.include_download_url:
            return img['description']
        return """%s (<a class="download" href="%s">Download</a>)""" %(
            img['description'],
            img.get('download_url', img.get('image_url')))
GalleriaSettings = createSettingsFactory(GalleriaDisplayType.schema)
