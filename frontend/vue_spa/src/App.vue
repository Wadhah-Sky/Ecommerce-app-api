<template>

<!--  <transition name="nested" mode="out-in">-->

    <!-- The element inside `<transition>` is expected to have a `v-if` or `v-show` directive -->
    <!-- I had a transition which worked with v-if but not with v-show. -->

    <div v-if="storeContentLoading.homeViewDataLoading || storeContentLoading.navSidebarDataLoading">

      <transition name="nested" mode="out-in">

        <logo-loading-view v-show="true"/>

      </transition>

    </div>

    <div v-else>

      <transition name="nested" mode="in-out">

        <div v-show="storeNavSidebar.show" id="nav-sidebar">

            <nav-sidebar-component :store-nav-sidebar="storeNavSidebar"/>

        </div>

      </transition>


      <div class="padding-x">

        <transition>

          <div v-show="true" id="nav">

              <navbar-component :store-home="storeHome"
                                :store-checkout="storeCheckout"
                                :show-cart-drop-down-menu="storeCheckout.showCartDropDownMenu"
                                :show-nav-sidebar="storeNavSidebar.show"
                                :toggle-nav-sidebar-view="storeNavSidebar.toggleNavSidebarView"
              />

          </div>

        </transition>

        <router-view name="default" v-slot="{ Component, route }" >

          <div v-if="errMsg" class="container mt-3">
            <h2 class="text-center">
              {{ errMsg }}
            </h2>
          </div>

          <div v-else>

            <transition :name=" route.meta.transition || 'nested' "
                        mode="out-in">
              <div v-show="true">
                <suspense :timeout="timeOut">

                  <template #default >

                    <component :is="Component"
                               :key="route.meta.usePathKey ? route.path : undefined"
                    >

                    </component>

                  </template>

                  <template #fallback>

                    <content-loader-component/>

                  </template>

                </suspense>
              </div>
            </transition>
          </div>

        </router-view>

        <transition name="nested" mode="out-in">

            <div v-show="true" id="footer" class="pt-5">
              <footer-component/>
            </div>

        </transition>

      </div>

    </div>

<!--  </transition>-->

</template>

<script>

/*
  Info: By design, JavaScript is a synchronous programming language. This means that when code
        is executed, JavaScript (within block of async) starts at the top of the file and runs
        through code line by line, until it is done.
        An async function can contain an await expression, that pauses the execution of the async
        function and waits for the passed Promise's resolution, and then resumes the async function's
        execution and returns the resolved value.
        So, Every async function returns a Promise object. The await statement operates on a Promise,
        waiting until the Promise resolves or rejects.
        You can't do tasks (without await) on the result of an async function directly, even if you
        use await when call that async function.
        Using await will make your function wait and then return a Promise which resolves immediately, but
        it won't unwrap the Promise for you. You still need to unwrap the Promise returned by the async
        function, either using 'await' or using '.then()'.
 */

/*
  What is the difference between 'window', 'screen', and 'document' in JavaScript?

  1- window is the main JavaScript object root, aka the global object in a browser, and it can also be treated
     as the root of the document object model. You can access it as window.

  2- window.screen or just screen is a small information object about physical screen dimensions.

  3- window.document or just document is the main object of the potentially visible (or better yet: rendered)
     document object model/DOM.

Since window is the global object, you can reference any properties of it with just the property name - so you do not have to write down window. - it will be figured out by the runtime.
 */

/*
 Note: If you want to use both of Vue 3 'Option' and 'Composition' API, then make sure to
       imports your libraries in <script> tag not in <script setup> since this could
       lead to an error:
       Crbug/1173575, non-JS module files deprecated.

       Also be notice if you don't set export value of your component, then you will
       face an issue with routing from one component to another especially when using
       Back or Forward buttons on the browser.
 */

/*
* Note: 'defineProps' and 'defineEmits' are compiler macros only usable inside <script setup>.
       They do not need to be imported, and are compiled away when <script setup> is processed.
       But, since we don't import them, the '@babel/eslint-parser' that install by default by Vue/Cli
       and defined as your project parser in '.eslintrc.js' file will raise an error:

       ESLint: 'defineProps' is not defined.(no-undef)

       So to solve it, just import the 'defineProps', even if Vue/Cli show a warning at compile time.
       INFO: DON'T try to change your parser to another one because will lead to another issues.
 */

/*
   Note: props that type Object or Array with default values should be:

         const props = defineProps({
               // Object with a default value
               propE: {
               type: Object,
               // Object or array defaults must be returned from
               // a factory function. The function receives the raw
               // props received by the component as the argument.
               default(rawProps) {
                 return { message: 'hello' }
               },

               // Custom validator function for type Array
               propF: {
                 type: Array
                 validator(value) {
                   // The value must match one of these strings
                   return ['success', 'warning', 'danger'].includes(value)
               }
          });
 */

/*
 Info: Unlike ref(), the inner value of a shallow ref is stored and exposed as-is, and will not be made
       (deeply) reactive. To reduce reactivity overhead for Large immutable structures like components or
       big arrays that contains thousands of objects.
*/

/* Note: if you faced a warning in your browser console:

        <Transition> renders non-element root node that cannot be animated

        probably forget to put the child components of <Transition> inside a <div>,
        Transitions require single children nodes. Therefore you can wrap the <component>
        tag inside a <div>, however, a plain <div> inside a <transition> won't trigger the
        transition, but changing the :key directive does.
        This will effectively transition between routes with a different name, but if you
        also want to transition between routes of the same name with different parameters,
        you can use route.fullPath instead of route.name as the key.
 */

/* Note: if you faced a warning in your browser console:
*
*        [Vue warn]: ＜Suspense＞ slots expect a single root node.
*
*        to solve it put <component> inside a <div> tag with :key directive which will make sure
*        each component is wrapped by its <div> tag.
*/

/* Important: if you have a view component that have children component, it's better to trigger
              the function of 'Pinia' stores and set state management variables at the parent
              component (view component) Not at the child component even if data related to him,
              because this will make sure no conflict will happen between siblings components
              and also will be easy to track code errors.
*/

/* How to update the url in the browser using Vue Router?

   1- by using <router-link>
   2- by using useRouter.push() or useRouterReplace()
      for example:
      useRouter.push({path: route.path, query: {...route.query, page: page} })
*/

/* Note: the Vue Router will render automatically the view using this new url if the new :key value
         that set to the <div> element which hold the <component> in <router-view> inside App.vue and
         this value can be set to be route.fullPath (in order to destroy the view and re-render it
         whenever the full path changed) or use route.path (the same thing whenever the path changed) or
         we can Not set the :key (in this case Vue router only re-render the view whenever we travel
         between views), so if this value is different from the current :key for current
         <div :key="?"><component/></div> value will destroy the view and re-render it again.
*/

/*
  Note: title attribute of any HTML element is related to the browser itself and changed by
        description aria ID and can't be dynamic, so the best way to have dynamic title is by
        creating a custom attribute and use it with any HTML element.
 */

/*
  Info: if you ever see an html element have attribute of data-v-<hashed_number>, this comes
        from css loader that selected as scoped, like when using <style scoped>
 */

/*
  The difference between v-model and v-bind?

  A directive that is commonly switched up with v-model is the v-bind directive.
  The difference between the two is that v-model provides two-way data binding.
  This means that if our data changes, our input will too, and if our input changes, our data changes too.
  However, v-bind only binds data one way. Meaning that we can pass data to a component, but if we type
  in our input - our original value won't be changed.
 */

/*
  How to use v-model with child component?
  1- in child component inputs add:

     A- directly emit signal ('update:modelValue') which is related to v-model attribute that will be
     received in parent component:

     @input="$emit('update:model-value', $event.target.value)"

     B- or through using a defined emits array:

     @input="emits('update:model-value', $event.target.value)"

     with define of emits in <script setup>:

     const emits = defineEmits(['update:model-value']);

  2- in parent component, define a ref value and using with v-model on child component:

     <parent-component>
       <child v-model="<name-of-ref-const>" />
     </parent>

  Note: the two steps above will update the data from child component to parent component only, in case
        you want two ways updating, then:

        1- add prop variable in the child component and name it like the emit name with camelCase style.

           const props = defineProps({modelValue: {type: Object, required: true},});

        2- Now you can process the prop 'modelValue' to be reactive:

           const modelValue = ref(props.modelValue);
 */

/*
   Note:
   1- Don't use same ref const (const el =ref(null)) as v-model const with multiple component fragments, this
      will cause to have multiple v-model that work separately from other fragments, this happened when using
      v-for in parent component to send data for child component those have v-model with their inputs,
      so, you will have multiple child component as fragments, to solve it:

      A- move v-for into child component, in this case will have one child component.
      B- use unique index for that ref variable with each fragment like using:
         <child v-model=el[index] />

   2- if you face such error:

      Extraneous non-props attributes (<name-of-emit>) were passed to component but could not be automatically
      inherited because component renders fragment or text root nodes.

      this means you passing out value from multiple child component to parent component, so you need to set root
      to these components by wrap them with <div>.
 */

/*
  what deference between ref and :ref ?

  ref : is static reference that can be used to hold ref of single/multiple elements and
        can be use with v-for, and remember to define its const as ref:

       <input v-for="el in elements" ref="inputs" />

       Note: you can't use array reference variable for multiple elements as shown above unless
             it's in v-for block otherwise you have to set each element a defined reference variable.

  :ref : this the dynamic reference that can be used to hold ref of single/multiple elements and
         can be use with v-for, and remember to define its const as ref:

         <input v-for="el in elements" :ref="inputs" />

         * The big deference that :ref is dynamic and can be change when component is updating,
           so be careful if you use it as array:

           <input v-for="el in elements" :ref="el => inputs.push(el)" />

           This will cause to keep updating the inputs with new duplicated references.
 */

/*
  Difference between watch() and watchEffect():

  1- watch by default can be used to lazily trigger while side effects (watchEffect is always immediate).
  2- watchEffect automatically watches for changes to any state changes (watch must be provided with
     a variable or variables to watch).
  3- watch provides access to the current and previous values.
  4- watch is shallow by default: the callback (your method) will only trigger when the watched property
     has been assigned a new value - it won't trigger on nested property changes. If you want the callback
     to fire on all nested mutations, you need to use {deep: true}.
  5- watch is lazy by default as we said above: the callback won't be called until the watched source has
     changed. But in some cases we may want the same callback logic to be run eagerly - for example, we
     may want to fetch some initial data, and then re-fetch the data whenever relevant state changes,
     so use {immediate: true}.
  6- When you mutate reactive state, it may trigger both Vue component updates and watcher callbacks created by you.
     By default, user-created watcher callbacks are called before Vue component updates. This means if you attempt
     to access the DOM inside a watcher callback, the DOM will be in the state before Vue has applied any updates.
     If you want to access the DOM in a watcher callback after Vue has updated it, you need to specify the
     {flush: 'post'} option.
  7- In the rare case where you need to stop a watcher before the owner component unmounts using:
     unwatch()
 */

/*
  What are watch() source types?

  watch's first argument can be different types of reactive "sources": it can be a ref (including computed refs),
  a reactive object, a getter function, or an array of multiple sources, e.g.

  >> const x = ref(0);
  >> const y = ref(0);

  // single ref
  >> watch(x, (newX) => {
  >>  console.log(`x is ${newX}`)
  >> });

  // getter
  >> watch(
  >>  () => x.value + y.value,
  >>  (sum) => {
  >>  console.log(`sum of x + y is: ${sum}`)
  >>  }
  >> );

  // array of multiple sources
  >> watch([x, () => y.value], ([newX, newY]) => {
  >>  console.log(`x is ${newX} and y is ${newY}`)
  >> });

  Do note that you can't watch a property of a reactive object like this:

  >> const obj = reactive({ count: 0 });

  // this won't work because we are passing a number to watch()
  >> watch(obj.count, (count) => {
  >>  console.log(`count is: ${count}`)
  >> });

  Instead, use a getter:

  >> watch(
  >> () => obj.count,
  >> (count) => {
  >>  console.log(`count is: ${count}`)
  >> }
  >> )

  * Note: we can't watch ref of property of constant object, e.g.

          const test = {x: ref(false)};

 */

/*
  is objects in javascript passed by reference or value?

  It's always pass by value, but for objects the value of the variable is a reference. Because of this,
  when you pass an object and change its members, those changes persist outside the function. This
  makes it look like pass by reference. But if you actually change the value of the object variable you
  will see that the change does not persist, proving it's really pass by value.

  Examples:

  function changeObject(x) {
    x = { member: "bar" };
    console.log("in changeObject: " + x.member);
  }

  function changeMember(x) {
    x.member = "bar";
    console.log("in changeMember: " + x.member);
  }

  var x = { member: "foo" };

  console.log("before changeObject: " + x.member);
  changeObject(x);
  console.log("after changeObject: " + x.member); // change did not persist

  console.log("before changeMember: " + x.member);
  changeMember(x);
  console.log("after changeMember: " + x.member); // change persists

 */

/*
  How do I correctly clone a JavaScript object?

  you can use in ES6:

  const clone = structuredClone(object);

 */

/*
  How to check that of current variable is an object created by => new Object() or notations {<key>: <value>}?

  Object.getPrototypeOf(<variable>) === Object.prototype
 */

/*
  If you ever come through below errors/warns:

  1- [vue warn]: inject() can only be used inside setup() or functional components.

     This happens due below block code in core code:

     else if ((process.env.NODE_ENV !== 'production')) {
        warn(`inject() can only be used inside setup() or functional components.`);
     }

  2- wthAsyncContext called without active current instance. This is likely a bug.

     This happens due there is promise that not caught by 'wait', probably due an error raise
     while processing the async method.

  3- caught (in promise) TypeError: Cannot read properties of null (reading 'scope')

     This error is the main reason for the 1 & 2 error if come together, and it happened when using
     vue-router with store management like 'Pinia', so far there is no clear answer for the cause of
     this issue, but you can minimize it by:

     1- make sure you probably defined the 'pinia' in 'main.js' file.
     2- import the stores of 'Pinia' as first in the related component and use the store only inside
        setup() stage of the component OR register it as global property for registered 'app'.
     3- make sure the local & network is available.
     4- restart the vue-cli by re-run the command: npm run serve

  4- [Vue warn]: There is already an app instance mounted on the host container. If you want to mount
                 another app on the same host container, you need to unmount the previous app by calling
                 app.unmount() first.

     This is the mean reason in add to the list mentioned above (4 reasons) for all faults that keep
     happens and make vue-router crash.
     finally, to solve this issue you should see if app (App.vue) is already mount, it's useful:

     1- When refresh the page, so you don't need to mount another app instance as Webpack server suggest
        in the warning.

     2- Will prevent trigger the methods these defined in App.vue <script setup> twice (one for update
        life-cycle of component and second when re-mount the component again, which happens when refresh
        the page).

     See the update code in 'main.js' file.
 */

/*
  How to update the child component that relate on store management state without need to
  watch the state inside that component?

  You have to pass the data as attribute/prop for the child component and since the 'props' are reactive
  by default so any change in the state from parent component will reflect on child component.
  Don't pass the store and then use toRef() method to make it reactive inside child component because this
  will not work and will not watch the mutation of the state for that store.
  But be careful if using <store>.$reset() inside parent component before leaving the route because this
  will raise an error in child component because it not dis-mount at that moment, so to solve this issue
  wrap the child component inside parent component with v-if for the related data, which means if this data
  not exist remove the component.

 */

/*
  What is difference between v-show and v-if?

  While v-if will stop something being rendered if the expression within it returns false ,
  v-show will still render the element - but it will apply display: none to the element.
 */

/*
  What is difference if used regex format with flag 'g' or not?

  'g' is the global search flag. The global search flag makes the RegExp search for a pattern
  throughout the string, creating an array of all occurrences it can find matching the given pattern.

  A very important side effect of this is if you are reusing the same regex instance against a matching
  string, it will eventually fail because it only starts searching at the 'lastIndex'.

  > 'aaa'.match(/a/g)
    [ 'a', 'a', 'a' ]

  > 'aaa'.match(/a/)
    [ 'a', index: 0, input: 'aaa' ]

  It will break things if you re-use the RegExp:
  > var r = /a/g;
  > console.log(r.test('a') // true
  > r.test('a')); // false
 */

/*
  Info: 1- if you set 'null' to any attribute of html tag or component boolean property, will
           remove that attribute/property.
        2- if you set empty string '' value to boolean html attribute or component boolean
           property, will consider as true.
        3- 'undefined' value consider as 'null' when set to html tag attribute or component
           boolean property.
 */

/*
  Info: If you are trying to get the data of pressed key, use:

        @input="<method($event.data)>"

        Or with:

        @keydown="<method($event.keyCode)>"

        And inside the method can get the character of 'keyCode':

        String.fromCharCode(keyCode)
 */

/*
  Note: Any html element is inserted using innerHTML property or v-html directive, its defined class style
        will be ignored and to solve that you need to set its style inside <style> tag that is NOT scoped.
 */

/*
  How to deal with string value of 'true'/'false' as boolean?

  Using the identity operator (===), which doesn't make any implicit type conversions when the compared
  variables have different types.

  You should probably be cautious about using these two methods for your specific needs:

  >> var myBool = Boolean("false");  // == true

  >> var myBool = !!"false";  // == true

  Note: Any string which isn't the empty string will evaluate to true by using them.
 */

/*
  Libraries, methods, variables and components imports
*/
// @ is an alias to /src
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useCheckoutStore} from "@/store/Checkout";
import {useContentLoadingStore} from "@/store/ContentLoading";
import {useHomeStore} from "@/store/Home";
import {useNavSidebarStore} from "@/store/NavSidebar";
import LogoLoadingView from "@/views/LogoLoadingView";
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import NavSidebarComponent from "@/components/NavSidebarComponent";
import NavbarComponent from "@/components/NavbarComponent";
import FooterComponent from "@/components/FooterComponent";
import {useRouter} from "vue-router";
import {ref, onErrorCaptured} from 'vue';

export default {
  name: "App",
  components: {
    LogoLoadingView,
    ContentLoaderComponent,
    NavbarComponent,
    NavSidebarComponent,
    FooterComponent
  }
};

</script>

<script setup>
// NOTE: setup is the first of life-cycle of any vue component, before the component is created.

/*
  Define handlers (properties, props and computed)
*/
const storeEndpoint = useEndpointStore();
const storeCheckout = useCheckoutStore();
const storeContentLoading = useContentLoadingStore();
const storeHome = useHomeStore();
const storeNavSidebar = useNavSidebarStore();
const router = useRouter();

/*
  Set the value for 'timeout' prop of <suspense>, to override behavior of display
  the previous #default content while waiting for the new content and its async
  dependencies to be resolved.
*/
const timeOut = 0;
const errMsg = ref(null);

/*
  Define functions
*/
const loadCheckoutInfo = async () => {
  /**
   * Load info from local storage into 'Checkout' store state.
   */

  // Get the cart json string from local storage api.
  // Note: local storage only work with strings, so we have to parse the json string into
  //       equivalent data type.

  // Mutate with $patch function.
  // Note: we set default value type the same as the initialize type in the store state,
  //       otherwise will cause an issue.
  storeCheckout.$patch((state) => {
    state.cartProducts = JSON.parse(window.localStorage.getItem("jamie&CassieCart")) || [];
    state.shippingDetails = JSON.parse(window.localStorage.getItem("jamie&CassieShippingDetails")) || {};
    state.paymentDetails = JSON.parse(window.localStorage.getItem("jamie&CassiePaymentDetails")) || {};

  });
};
const refreshCartItems = async () =>{
  /**
   * Method to refresh cart product items details from backend server.
   */

  /*
     Note: the same method is being use inside 'CheckoutView.vue', so in case the current
           route path of router is pointing on the route of that view, we don't want to
           trigger same code of method twice (one in App.vue because it's root component and
           second in CheckoutView.vue) specially when you refresh the page when you on
           'CheckoutView.vue'.
   */

  /*
     Info: By using matched() method, get the path name of parent for current route, if it's
           'checkout' (this is what we define in 'index.js' file for 'CheckoutView.vue') so we count
           on the method that implement same concept inside that view and no need to trigger the one
           inside root component.
   */
  if(router.currentRoute.value.matched[0].name !== 'checkout') {
    // Update the cart items details from backend server.
    await storeCheckout.refreshCartItems(storeEndpoint.cartCheckEndpoint);
  }
};
const triggerGetDataResult = async () => {
  /**
   * Get all data list from backend server for the frontend landing homepage.
   */

  await storeHome.getDataResult(storeEndpoint.homeEndpoint);
  await storeNavSidebar.getDataResult(storeEndpoint.storeCategoriesEndpoint);
};

// initialize steps of App.vue
/*
     Important: Since our child components of App.vue using vue-router methods like
                useRoute() and useRouter() and depend on info these methods provide,
                and because the router hasn't yet completely resolved the initial navigation
                when you enter/refresh the page, so route refers to the default (/) initially
                in your methods that depend on.
                Vue Router's isReady() method returns a Promise that resolves when the router
                has completed the initial navigation,

     Note: if you didn't do this step will face issue when navigate between views
           and vue router will throw an exception (usually).
 */
router.isReady().then(()=>{
  // Here we wrap method calls without await in then wrap that will make sure to run these
  // method when a promise is return by isReady().

  /*
    call functions
   */
  triggerGetDataResult();
  loadCheckoutInfo();
  refreshCartItems();
});

/*
  call imported method
*/
onErrorCaptured(() => {
  errMsg.value = "Something went wrong!";
});

</script>

<style lang="scss">

/*
  Note: The focusout event fires when an element has lost focus, after the blur event.
        The two events differ in that focusout bubbles (means detect by child elements), while blur does not.
        The opposite of focusout is the focusin event, which fires when the element has received focus.
        The focusout event is not cancelable.
 */

/*
 If you want to override Sass variables of specific imported file:
 1- Change value of variables.
 2- Import the file.

 Note: if you import the file in App.vue component, you don't need to
       import it in main.js file.
 */

$color-1: #0F1111;
$color-2: #fff;
$color-3: #464646;
$color-4: #e9ecef;

/* BootStrap */
$pagination-color: $color-3;
$pagination-focus-bg: $color-4;
$pagination-hover-color: $color-3;
$pagination-hover-bg: $color-4;
$pagination-active-color: $color-2;
$component-active-bg: $color-1;
$pagination-focus-color: $color-3;
$pagination-disabled-color: $color-3;
$pagination-disabled-bg: $color-4;

$form-check-label-color: $color-3;
$form-check-label-cursor: pointer;

$tooltip-color: $color-2;
$tooltip-bg: $color-1;

$input-color: $color-3;
$input-bg: $color-2;

$input-border-radius: 0;
$input-border-color: $color-1;
@import "bootstrap";

/* vue-sidebar-menu */
$primary-color: $color-1;
$base-bg: $color-2;
$base-color: $color-3;
$base-hover-bg-color: $color-4;

$item-color: $base-color;
$item-active-color: $base-color;
$item-hover-color: $base-color;
$item-hover-bg: $base-hover-bg-color;
$item-open-color: $base-bg;
$item-open-bg: $primary-color;
$icon-bg: $base-hover-bg-color;
$icon-active-color: $base-bg;
$icon-active-bg: $primary-color;
$toggle-btn-color: $primary-color;
@import "vue-sidebar-menu/src/scss/vue-sidebar-menu.scss";

/* Maz ui */
:root {
  --maz-color-black: hsl(180, 6%, 6%)!important;
  --maz-color-black-contrast: hsl(0deg 0% 100%)!important;
}

.--bottom{
  max-width: 240px!important;
  max-height: 250px!important;
}

.m-phone-number-input__input{
  width: 100%!important;
}

/* This will effect all Maz input in parent and children components */
.m-input-wrapper{
  border-radius: 0!important;
}

.m-input-label {
  font-weight: 400!important;
  color: #0f1111!important;
  font-size: 14px!important;
}

.m-select-list{
  border-radius: 0!important;
  width: 100%!important;
}

.m-select-list .--is-selected{
  background-color: #0f1111!important;
  color: #fff!important;
}

.shipping-method .m-input-wrapper-input,
.shipping-method .m-input-wrapper-right,
.shipping-method .m-select-list{
  background-color: rgb(247, 247, 247)!important;
  outline: none!important;
}

@import "maz-ui/css/main.css";

</style>

<style>

body {
  font-family: 'Noto Sans JP', sans-serif;
  font-weight: 300;
  max-height: 100vh;
  overflow-y: auto;
}

::-webkit-scrollbar {
  width: 6px;
  border-radius: 4px;
  z-index: 99;
  opacity: 0;
  transition: 0.3s opacity ease;
}

/* Track */
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px #aaa;
    -webkit-border-radius: 4px;
    border-radius: 4px;
    cursor: pointer;

}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 4px;
  border-radius: 4px;
  background: #0F1111;
  -webkit-box-shadow: inset 0 0 6px #aaa;
  transform: translate(0%);
  display: block;
  opacity: 1;
  cursor: pointer;
  user-select: none;
  transition: 0.3s opacity ease;
}

input[type="search"]::-webkit-search-cancel-button {

  /* Remove default */
  -webkit-appearance: none;
  appearance: none;

  /* Now your own custom styles */
  height: 24px;
  width: 24px;
  margin-left: .4em;
  cursor: pointer;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23777'><path d='M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'/></svg>");

}

input[type="search"]::-webkit-search-cancel-button:hover{
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='rgb(204, 12, 57)'><path d='M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'/></svg>")!important;
  transition: 200ms all ease-in-out;
}

/*!* Override the black color of Maz input *!*/
/*:root {*/
/*  --maz-color-black: hsl(180, 6%, 6%)!important;*/
/*  --maz-color-black-contrast: hsl(0deg 0% 100%)!important;*/
/*}*/

/*.--bottom{*/
/*  max-width: 240px!important;*/
/*  max-height: 250px!important;*/
/*}*/

/*.m-phone-number-input__input{*/
/*  width: 100%!important;*/
/*}*/

/*!* This will effect all Maz input in parent and children components *!*/
/*.m-input-wrapper{*/
/*  border-radius: 0!important;*/
/*}*/

/*.shipping-method .m-input-wrapper-input,*/
/*.shipping-method .m-input-wrapper-right,*/
/*.shipping-method .m-select-list{*/
/*  background-color: rgb(247, 247, 247)!important;*/
/*  outline: none;*/
/*}*/

/*.shipping-method .m-select-list{*/
/*  width: 100%!important;*/
/*}*/

/*.m-input-label {*/
/*  font-weight: 400;*/
/*  color: #0f1111;*/
/*  font-size: 14px;*/
/*}*/

/*End of Maz customization*/

/* for phones and tablets */
@media(max-width:767px){
  .m-phone-number-input{
    display: block!important;
  }
  .m-phone-number-input__country-flag{
    margin-bottom: 58px!important;
  }
  .m-phone-number-input__select{
    display: inline-block!important;
  }
  .m-phone-number-input__input{
    display: inline-block!important;
    margin-left: 2px!important;
    margin-top: 8px!important;
  }
}

/* Transition rules that target nested elements */

/*When element enter the page*/
.nested-enter-from{
  opacity: 0;
}

.nested-enter-to{
  opacity: 1;
}

/*When element exit the page*/
.nested-leave-from{
  opacity: 1;
}
.nested-leave-to{
  opacity: 0;
}

</style>
