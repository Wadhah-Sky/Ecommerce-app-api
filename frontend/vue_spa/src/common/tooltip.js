/* Create Bootstrap 5 tooltip directive for Vue to be use by any HTML
   element 'title' or 'data-bs-title.

 Note: import this element and then add it as directive to your app in main.js file:

      app.directive('tooltip', tooltip);
 */

import { Tooltip } from 'bootstrap';

export const tooltip = {
  // Called after the DOM has been mounted or rendered. Here you have access to
  // the DOM elements and DOM manipulation can be performed for example get the
  // innerHTML
  mounted(el) {
    new Tooltip(el, {
        container: 'body',
        trigger : 'hover'
    });
  }

};
