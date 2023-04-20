/*
  Register the bootstrap as global
  Note: local registration is when you import the file in a certain vue
        component rather than root component.

  Q/ What difference between mini.css and bootstrap.css file?
  A/ bootstrap.min.css has been minified. This means all the whitespace and other
     extra characters have been removed. This is commonly done for use in production,
     to reduce the size of the file. When developing, it is usually helpful to use
     the unminified version, since, as you said, it is readable.
*/
/*
   Note: You can also register them as global in App.vue file in
   <style> or <style lang=sass> specifically if you want to override sass
   variables value.
*/
// import "bootstrap/dist/css/bootstrap.min.css";
// import "bootstrap";

// Register Font Awesome library and svg-gif-png icons.
import { library } from '@fortawesome/fontawesome-svg-core';
// 'faS' class means 'fa-solid'.
import {
    faS,
    faSliders, faUser, faHouse, faStore, faHeadset, faEnvelope, faChevronRight,
    faChevronLeft, faShoppingCart, faCircleXmark, faCircleCheck, faXmark,
    faCircleExclamation, faStar, faCartShopping, faSpinner
} from '@fortawesome/free-solid-svg-icons';

// Register CSS/scss/sass and other files of your project as global.
/*
   Note: You can also register CSS/scss/sass files as global in App.vue file in
   <style> or <style lang=sass> specifically if you want to override sass
   variables value.
*/
// import 'swiper/swiper-bundle.css';
import 'swiper/css';
import 'swiper/css/navigation';

// import 'vue-sidebar-menu/dist/vue-sidebar-menu.css';
import './assets/css/ui.css';
import 'vue-multiselect/dist/vue3-multiselect.css';

// Import methods and component.
import { createApp } from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import { createPinia } from 'pinia';
import router from './router';
import VueSidebarMenu from 'vue-sidebar-menu';
import VueAgile from 'vue-agile';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {Multiselect} from 'vue-multiselect';
import {tooltip} from "@/common/tooltip";
import VueLazyload from 'vue-lazyload';
// import './plugins/bootstrap-vue';

/*
    Add the svg-gif-png icons those want to use with your Font Awesome library (utility
    class), so you don't to import all icons svg-gif-png files and minimize the space
    of use.
*/
library.add(
    faS,
    faSliders, faUser, faHouse, faStore, faHeadset, faEnvelope, faChevronRight,
    faChevronLeft, faShoppingCart, faCircleXmark, faCircleCheck, faXmark,
    faCircleExclamation, faStar, faCartShopping, faSpinner
);

// Vue lazy loader options.
const loadImage = require('./assets/images/svg-gif-png/loading.gif');
const errorImage = require('./assets/images/svg-gif-png/Image_not_available.png');

// Create vue App.
const app = createApp(App);

// Install the required instances as a plugin, component and directive.
app.use(createPinia());
app.use(router);
app.use(VueSidebarMenu);
app.use(VueAgile);
// 'preLoad' option is proportion of pre-loading height, default (1.3).
app.use(VueLazyload, {
  preLoad: 1.3,
  loading: loadImage,
  error: errorImage,
  attempt: 3
});
app.component('font-awesome-icon', FontAwesomeIcon);
app.component('multi-select', Multiselect);
app.directive('tooltip', tooltip);

// Mount 'app' as root component.
app.mount('#app');


