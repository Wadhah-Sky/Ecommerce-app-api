<template>

<!--  <transition name="nested" mode="out-in">-->

    <div v-if="storeContentLoading.homeViewDataLoading || storeContentLoading.navSidebarDataLoading"


    >

      <transition name="nested" mode="out-in">

        <logo-loading-view/>

      </transition>

    </div>

    <div v-else>

      <transition name="nested" mode="out-in">

        <div id="nav-sidebar">

            <nav-sidebar-component/>

        </div>

      </transition>


      <div class="padding-x">

        <transition name="nested" mode="out-in">

          <div id="nav">

              <navbar-component/>

          </div>

        </transition>

        <router-view name="default" v-slot="{ Component, route }">

          <div v-if="errMsg" class="container mt-3">
            <h2 class="text-center">
              {{ errMsg }}
            </h2>
          </div>

          <div v-else>

            <transition :name=" route.meta.transition || 'nested' "
                        mode="out-in">
              <div>
                <suspense :timeout="timeOut">

                  <template #default>

                    <component :is="Component"
                               :key="route.meta.usePathKey ? route.path : undefined">

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

<!--        <router-view name="default" v-slot="{ Component, route }">-->

<!--          <div >-->

<!--            <transition :name=" route.meta.transition || 'nested' " mode="out-in">-->
<!--              <div :key="route.path">-->

<!--                      <component :is="Component"-->
<!--                                 :key="route.meta.usePathKey ? route.path : undefined"-->
<!--                      >-->

<!--                      </component>-->
<!--                -->
<!--              </div>-->
<!--            </transition>-->

<!--          </div>-->

<!--        </router-view>-->

        <transition name="nested" mode="out-in">

        </transition>

        <transition name="nested" mode="out-in">

            <div id="footer" class="pt-5">
              <footer-component/>
            </div>

        </transition>

      </div>

    </div>

<!--  </transition>-->

</template>

<script>

/*
* Note: If you want to use both of Vue 3 'Option' and 'Composition' API, then make sure to
*       imports your libraries in <script> tag not in <script setup> since this could
*       lead to an error:
*       Crbug/1173575, non-JS module files deprecated.
*
*       Also be notice if you don't set export value of your component, then you will
*       face an issue with routing from one component to another especially when using
*       Back or Forward buttons on the browser.
*/

/*
* Note: 'defineProps' and 'defineEmits' are compiler macros only usable inside <script setup>.
*       They do not need to be imported, and are compiled away when <script setup> is processed.
*       But, since we don't import them, the '@babel/eslint-parser' that install by default by Vue/Cli
*       and defined as your project parser in '.eslintrc.js' file will raise an error:
*
*       ESLint: 'defineProps' is not defined.(no-undef)
*
*       So to solve it, just import the 'defineProps', even if Vue/Cli show a warning at compile time.
*       INFO: DON'T try to change your parser to another one because will lead to another issues.
*/

/*
 Info: Unlike ref(), the inner value of a shallow ref is stored and exposed as-is, and will not be made
       (deeply) reactive. To reduce reactivity overhead for Large immutable structures like components or
       big arrays that contains thousands of objects.
*/

/* Note: if you faced a warning in your browser console:
*
*        <Transition> renders non-element root node that cannot be animated
*
*        probably forget to put the child components of <Transition> inside a <div>,
*        Transitions require single children nodes. Therefore you can wrap the <component>
*        tag inside a <div>, however, a plain <div> inside a <transition> won't trigger the
*        transition, but changing the :key directive does.
*        This will effectively transition between routes with a different name, but if you
*        also want to transition between routes of the same name with different parameters,
*        you can use route.fullPath instead of route.name as the key.
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

     directly emit signal ('update:modelValue') which is related to v-model attribute that will be
     received in parent component:

     @input="$emit('update:modelValue', $event.target.value)"

     or through using a defined emits array:

     @input="emits('update:modelValue', $event.target.value)"

     with define of emits in <script setup>:

     const emits = defineEmits(['update:modelValue']);

     2- in parent component, define a ref value and using with v-model on child component:

     <parent-component>
       <child v-model="<name-of-ref-const>" />
     </parent>
 */

/*
   Note:
   1- Don't use same ref const as v-model const with multiple component fragments, this will cause
      to have multiple v-model that work separately from other fragments, this happened when using
      v-for in parent component to send data for child component those have v-model with their inputs,
      so, you will have multiple child component as fragments, to solve it move v-for into child component,
      in this case will have one child component.
   2- if you face such error:

      Extraneous non-props attributes (<name-of-emit>) were passed to component but could not be automatically
      inherited because component renders fragment or text root nodes.

      this means you passing out value from multiple child component to parent component, so you need to set root
      to these components by wrap them with <div>.
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
  Libraries, methods, variables and components imports
*/
// @ is an alias to /src
import {ref, onErrorCaptured} from 'vue';
import {useContentLoadingStore} from "@/store/ContentLoading";
import {useHomeStore} from "@/store/Home";
import {useNavSidebarStore} from "@/store/NavSidebar";
import {useEndpointStore} from "@/store/StaticEndpoint";
import LogoLoadingView from "@/views/LogoLoadingView";
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import NavSidebarComponent from "@/components/NavSidebarComponent";
import NavbarComponent from "@/components/NavbarComponent";
import FooterComponent from "@/components/FooterComponent";

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
/*
Set the value for 'timeout' prop of <suspense>, to override behavior of display
the previous #default content while waiting for the new content and its async
dependencies to be resolved.
*/
const storeContentLoading = useContentLoadingStore();
const storeHome = useHomeStore();
const storeNavSidebar = useNavSidebarStore();
const storeEndpoint = useEndpointStore();
const timeOut = 0;
const errMsg = ref(null);

/*
  Define functions
*/
const triggerGetDataResult = async () => {
  /**
   * Get all data list from backend server for the frontend landing homepage.
   */

  await storeHome.getDataResult(storeEndpoint.HomeEndpoint);
  await storeNavSidebar.getDataResult(storeEndpoint.storeCategoriesEndpoint);
};

/*
  call imported method
*/
onErrorCaptured(() => {
  errMsg.value = "Something went wrong!";
});

/*
  call functions
*/
triggerGetDataResult();

</script>

<style lang="sass">

/*
 If you want to override Sass variables of specific imported file:
 1- Change value of variables.
 2- Import the file.

 Note: if you import the file in App.vue component, you don't need to
       import it in main.js file.
 */

$color-1: #0F1111
$color-2: #fff
$color-3: #464646
$color-4: #e9ecef

/* BootStrap */
$pagination-color: $color-3
$pagination-focus-bg: $color-4
$pagination-hover-color: $color-3
$pagination-hover-bg: $color-4
$pagination-active-color: $color-2
$component-active-bg: $color-1
$pagination-focus-color: $color-3
$pagination-disabled-color: $color-3
$pagination-disabled-bg: $color-4

$form-check-label-color: $color-3
$form-check-label-cursor: pointer

$tooltip-color: $color-2
$tooltip-bg: $color-1

$input-color: $color-3
$input-bg: $color-2
@import "bootstrap"

/* vue-sidebar-menu */
$primary-color: $color-1
$base-bg: $color-2
$base-color: $color-3
$base-hover-bg-color: $color-4

$item-color: $base-color
$item-active-color: $base-color
$item-hover-color: $base-color
$item-hover-bg: $base-hover-bg-color
$item-open-color: $base-bg
$item-open-bg: $primary-color
$icon-bg: $base-hover-bg-color
$icon-active-color: $base-bg
$icon-active-bg: $primary-color
$toggle-btn-color: $primary-color
@import "vue-sidebar-menu/src/scss/vue-sidebar-menu.scss"

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

/*When element is active*/
.nested-enter-active,
.nested-leave-active{
  transition: all 0.3s ease-in-out;
}

</style>
