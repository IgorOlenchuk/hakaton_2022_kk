(function() {

	function Slideshow( element ) {
		this.el = document.querySelector( element );
		this.init();
	}

	Slideshow.prototype = {
		init: function() {
			this.wrapper = this.el.querySelector( ".slider-wrapper" );
			this.slides = this.el.querySelectorAll( ".slide" );
			this.previous = this.el.querySelector( ".slider-previous" );
			this.next = this.el.querySelector( ".slider-next" );
			this.index = 0;
			this.total = this.slides.length;

			this.actions();
		},
		_slideTo: function( slide ) {
			var currentSlide = this.slides[slide];
			currentSlide.style.opacity = 1;

			for( var i = 0; i < this.slides.length; i++ ) {
				var slide = this.slides[i];
				if( slide !== currentSlide ) {
					slide.style.opacity = 0;
				}
			}
		},
		actions: function() {
			var self = this;
			self.next.addEventListener( "click", function() {
				self.index++;
				self.previous.style.display = "block";

				if( self.index == self.total - 1 ) {
					self.index = self.total - 1;
					self.next.style.display = "none";
				}

				self._slideTo( self.index );

			}, false);

			self.previous.addEventListener( "click", function() {
				self.index--;
				self.next.style.display = "block";

				if( self.index == 0 ) {
					self.index = 0;
					self.previous.style.display = "none";
				}

				self._slideTo( self.index );

			}, false);
		}


	};

	document.addEventListener( "DOMContentLoaded", function() {

		var slider = new Slideshow( "#main-slider" );

	});


})();
