/**
 * @preserve Galleria Fullscreen Theme 2012-01-25
 * http://galleria.aino.se
 *
 * Copyright (c) 2011, Aino
 * Copyright (c) 2012, Petri Damstén
 * Licensed under the MIT license.
 *
 * Modified to work with Wordpress galleria-fs by Petri Damstén
 */

/* global jQuery, Galleria */

Galleria.requires(1.26, 'This version of theme requires Galleria 1.2.6 or later');

(function($) {

Galleria.addTheme({
    name: 'galleria-fs',
    author: 'Petri Damstén',
    css: 'galleria-fs.css',
    defaults: {
        transition: 'slide',
        thumbCrop:  'height',

        // set this to false if you want to show the caption all the time:
        _toggleInfo: false
    },
    init: function(options) {

        // add some elements
        this.addElement('info-link','info-close');
        this.append({
            'info' : ['info-link','info-close']
        });

        this.addElement('close', 'map', 'map-close');
        this.appendChild('container', 'close');
        this.appendChild('container', 'map');
        this.appendChild('map', 'map-close');

        // cache some stuff
        var info = this.$('info-link,info-close,info-text'),
            close = this.$('close'),
            map   = this.$('map'),
            map_close = this.$('map-close'),
            touch = Galleria.TOUCH,
            click = touch ? 'touchstart' : 'click';

        // show loader & counter with opacity
        this.$('loader, counter').show().css('opacity', 0.7);

        // some stuff for non-touch browsers
        if (! touch ) {
            this.addIdleState( this.get('image-nav-left'), { opacity:0 });
            this.addIdleState( this.get('image-nav-right'), { opacity:0 });
            this.addIdleState( this.get('counter'), { opacity:0 });
            this.addIdleState( this.get('info-link'), { opacity:0 });
            this.addIdleState( this.get('info-text'), { opacity:0 });
            this.addIdleState( this.get('thumbnails'), { opacity:0.25 });
        } else {
            this.$('image-nav-left, image-nav-right').hide();
        }
        this.addIdleState( this.get('close'), { opacity:0 });
        var gallery = this;
        $.each(this._layers, function() {
          gallery.addIdleState(this, {opacity:0});
        });

        // toggle info
        if ( options._toggleInfo === true ) {
            info.bind( click, function() {
                info.toggle();
            });
        } else {
            info.show();
            this.$('info-link, info-close').hide();
        }

        map.attr('id', 'galleria-map'); // openlayers needs id
        close.bind(click, function() {
            if ($('#galleria-map').is(":visible")) {
              $('#galleria-map').toggle();
            }
            $('#galleria').toggle();
        });
        map_close.bind(click, function() {
            $('#galleria-map').toggle();
        });

        // bind some stuff
        this.bind('thumbnail', function(e) {
            if (! touch ) {
                // fade thumbnails
                $(e.thumbTarget).css('opacity', 0.6).parent().hover(function() {
                    $(this).not('.active').children().stop().fadeTo(100, 1);
                }, function() {
                    $(this).not('.active').children().stop().fadeTo(400, 0.6);
                });

                if ( e.index === this.getIndex() ) {
                    $(e.thumbTarget).css('opacity',1);
                }
            } else {
                $(e.thumbTarget).css('opacity', this.getIndex() ? 1 : 0.6);
            }
        });

        this.bind('loadstart', function(e) {
            if (!e.cached) {
                this.$('loader').show().fadeTo(200, 0.4);
            }

            this.$('info').toggle( this.hasInfo() );

            $(e.thumbTarget).css('opacity',1).parent().siblings().children().css('opacity', 0.6);
        });

        this.bind('loadfinish', function(e) {
            this.$('loader').fadeOut(200);
        });
    }
});

}(jQuery));
