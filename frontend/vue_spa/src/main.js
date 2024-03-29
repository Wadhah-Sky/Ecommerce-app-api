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
    faCircleExclamation, faStar, faCartShopping, faSpinner, faArrowRight,
    faHandHoldingDollar, faCreditCard, faEye, faEyeSlash, faMagnifyingGlass,
    faPhone, faLocationDot
} from '@fortawesome/free-solid-svg-icons';
import {
    faAmazonPay, faCcAmazonPay, faCcMastercard, faCcVisa, faAlipay, faApplePay,
    faCcApplePay, faPaypal, faCcPaypal, faGooglePay, faStripe, faCcStripe,
    faFacebookF, faInstagram, faYoutube
} from '@fortawesome/free-brands-svg-icons';

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

// Import vue multiselect css files.
// import 'vue-multiselect/dist/vue3-multiselect.css'; // not working after update.
import 'vue-multiselect/dist/vue-multiselect.css';

// Import Maz-ui css files, we prefer to import it in App.vue style.
// import 'maz-ui/css/main.css';

// Import you css file as last style file.
import './assets/css/ui.css';

// Note: before everything else except the style files, import methods and components.

// Import methods and component.
import { createApp } from 'vue';
import App from './App.vue';
import { createPinia } from 'pinia';
import './registerServiceWorker';
import router from './router';
import VueSidebarMenu from 'vue-sidebar-menu';
import VueAgile from 'vue-agile';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {Multiselect} from 'vue-multiselect';
import { tooltip } from "@/common/tooltip";
import VueLazyload from 'vue-lazyload';
import MazPhoneNumberInput from 'maz-ui/components/MazPhoneNumberInput';
import MazInput from 'maz-ui/components/MazInput';
import MazSelect from 'maz-ui/components/MazSelect';
import { IMaskDirective } from 'vue-imask';
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
    faCircleExclamation, faStar, faCartShopping, faSpinner, faArrowRight,
    faHandHoldingDollar, faCreditCard, faEye, faEyeSlash,
    faAmazonPay, faCcAmazonPay, faCcMastercard, faCcVisa, faAlipay, faApplePay,
    faCcApplePay, faPaypal, faCcPaypal, faGooglePay, faStripe, faCcStripe,
    faMagnifyingGlass, faPhone, faLocationDot, faFacebookF, faInstagram,
    faYoutube
);

// Vue lazy loader options.
const loadImage = require('./assets/images/svg-gif-png/loading.gif');
const errorImage = require('./assets/images/svg-gif-png/Image_not_available.png');

// Initialize the variable that will be reference to new creating or existing 'App.vue' component.
let app = '';
// Set the name of HTML element id.
const containerSelector = "#app";

/*
  Note: If you don't want to use the existing 'app' instance, you can change the code
        by use 'app.unmount()' inside if{} block and remove else{} block, then outside
        the condition block plug in your components, stores..etc to the new created app
        instance and use 'app.mount(containerSelector)' at the end.
 */
// Get the #app element from DOM using querySelector() method.
const mountPoint = document.querySelector(containerSelector);

// check if app has been mounted already.
if (mountPoint && mountPoint.__vue_app__ !== undefined) {

    // Set the existing mount point to 'app'.
    app = mountPoint.__vue_app__._instance.proxy;
}
else {

    // create a new app instance
    app = createApp(App);

    // Create 'Pinia' instance.
    const pinia = createPinia();

    /*
       Info: You can register global property/properties to 'app' like register stores, so you
             can use them directly in the project components.
     */
    // app.config.globalProperties.<namedStore> = <useNamedStore()>;

    // Install the required instances like plugin, component and directive.
    app.use(router);
    app.use(pinia);
    app.use(VueSidebarMenu);
    app.use(VueAgile);
    // 'preLoad' option is proportion of a pre-loading height, default (1.3).
    app.use(VueLazyload, {
        preLoad: 1.3,
        loading: loadImage,
        error: errorImage,
        attempt: 3
    });
    app.component('font-awesome-icon', FontAwesomeIcon);
    app.component('multi-select', Multiselect);
    app.component('maz-input', MazInput);
    app.component('maz-select', MazSelect);
    app.component('maz-phone-number-input', MazPhoneNumberInput);
    app.directive('tooltip', tooltip);
    app.directive('imask', IMaskDirective);

    // Mount 'app' const (App.vue) as root component.
    /* Note: mount() function returns void and not the Vue app instance. You must separately
             call the app.mount() method when creating a Vue app in a fluent method call
             chain to keep reference to the Vue app instance.
     */
    app.mount(containerSelector);
}
