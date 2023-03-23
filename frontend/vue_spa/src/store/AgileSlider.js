import { defineStore, acceptHMRUpdate } from 'pinia';


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/


/*
 Screen Size : Phone (0px up to 600px), Tablet (600px up to 900px), PC (above 900px)
*/


/**
 *
 * Parameter           Type       Default                   Description
 * ---------         ---------  ----------             --------------------
 * asNavFor            array        []         Set the carousel to be the navigation of other carousels
 * autoplay           boolean      false       Enable autoplay
 * autoplaySpeed    integer (ms)   3000        Autoplay interval in milliseconds
 * centerMode         boolean      false       Enable centered view when slidesToShow > 1
 * changeDelay      integer (ms)    0          Insert a delay when switching slides. Useful for fade: true
 * dots               boolean      true        Enable dot indicators/pagination
 * fade               boolean      false       Enable fade effect
 * infinite           boolean      true        Infinite loop sliding
 * initialSlide       integer       0          Index of slide to start on
 * mobileFirst        boolean      true        Enable mobile first calculation for responsive settings
 * navButtons         boolean      true        Enable prev/next navigation buttons
 * options            object       null        All settings as one object
 * pauseOnDotsHover   boolean      false       Pause autoplay when a dot is hovered
 * pauseOnHover       boolean      true        Pause autoplay when a slide is hovered
 * responsive         object       null        Object containing breakpoints and settings objects
 * rtl                boolean      false       Enable right-to-left mode
 * slidesToShow       integer       1          Number of slides to show
 * speed            integer (ms)   300         Slide animation speed in milliseconds
 * swipeDistance    integer (px)    50         Distance to swipe the next slide
 * throttleDelay    integer (ms)   500         Throttle delay for actions
 * timing             string       ease        Transition timing function (linear/ease/ease-in/ease-out/ease-in-out)
 * unagile           boolean       false       Disable Agile carousel
 *
 */

export const useAgileSliderStore = defineStore('AgileSlider', {
  state: () => ({
      options: {
          /* Global settings (will consider the default setting for smartphones
             with screen size less than 600px). */
          autoplay: true,
          autoplaySpeed: 7000,
          changeDelay: 0,
          navButtons: false,
          speed: 3000,
          fade: true,
          dots: false,
          // Configure global settings to be responsive to screen size of tablet and PC.
          responsive: [
              {
                  // overwritten default global settings when the screen size is over 600px.
                  breakpoint: 600,
                  settings: {
                      dots: true
                  }
              },
              {
                  // overwritten default global settings when the screen size is over 900px.
                  breakpoint: 900,
                  settings: {
                      dots: true,
                      pauseOnDotsHover: true
                  }
              }
          ]
      }

  }),
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useAgileSliderStore, import.meta.hot))
}