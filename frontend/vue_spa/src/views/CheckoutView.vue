<template>

  <section class="section-content mt-5 bg-white">

    <div class="container">

      <div class="row pt-3">

        <main class="col-md-12">

          <header class="border-bottom mb-3 ms-0 pb-2">

            <div class="row justify-content-center">
              <div class="col-md-9">
                <ul class="bc">

                  <li :class="['bc_item', views['cart'] ? 'bc_complete' : '']">

                    <router-link v-if="views['cart']" :to="{name: 'cart'}">
                      Cart
                    </router-link>

                    <span v-else>Cart</span>

                  </li>

                  <li :class="['bc_item', views['shippingDetails'] ? 'bc_complete' : '']">

                    <router-link v-if="views['shippingDetails']" :to="{name: 'shippingDetails'}">
                      Shipping Details
                    </router-link>

                    <span v-else>Shipping Details</span>

                  </li>

                  <li :class="['bc_item', views['paymentDetails'] ? 'bc_complete' : '']">

                    <router-link v-if="views['paymentDetails']" :to="{name: 'paymentDetails'}">
                      Payment Details
                    </router-link>

                    <span v-else>Payment Details</span>

                  </li>

                  <li class="bc_item">Order</li>

                </ul>
              </div>
            </div>

          </header>

        </main>

      </div>

    </div>

  </section>

    <div class="main">

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

    </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
// @ is an alias to /src
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useCheckoutStore} from "@/store/Checkout";
import { MutationType } from 'pinia';
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import { useRouter, onBeforeRouteLeave, onBeforeRouteUpdate} from "vue-router";
import {ref, onErrorCaptured} from 'vue';

export default {
  name: "CheckoutView",
  components:{
    ContentLoaderComponent
  }
}
</script>

<script setup>

/*
 Note: 'onBeforeRouteUpdate' guard can be use when trying to update the current route url (path), while
       'onBeforeRouteLeave' can be use when trying to leave the current route (path) to another route (path).

       Both of them should be at top of setup().
*/
onBeforeRouteUpdate(async (to, from, next) => {

  /*
    Note: You must call next() exactly once in any given pass through a navigation guard.
          It can appear more than once, but only if the logical paths have no overlap, otherwise
          the hook will never be resolved or produce errors.
   */

  /*
    Info: notice that we are use return statement here to call next(), to prevent calling code
          after the statement.
   */

  // Check that to.name is included within 'view' reference object.
  if(Object.keys(views.value).includes(String(to.name))){

    // Set and check if 'to.name' to be true if fulfills the requirements.
    await setViews(to.name);

    // if views for 'to.name' is false, set 'to.name' to be 'cart'.
    if(views.value[to.name] === false){
      // redirect to 'cart' view.
      // Note: redirect will not change the original url path
      return next({path: '/checkout/cart'});
    }
    else{
      return next();
    }
  }
  else {
    // Default router push;
    return next();
  }
});

onBeforeRouteLeave(() => {
  // Reset some state variables of storeCheckout using patch function.
  storeCheckout.$patch((state) => {
    state.cartApiCouponCode = '';
    state.cartApiErrorMsg = '';
  });
});

/*
  Define handlers (properties, props and computed)
*/
const storeEndpoint = useEndpointStore();
const storeCheckout = useCheckoutStore();
const router = useRouter();
// const route = useRoute();
const timeOut = 0;
const errMsg = ref(null);
// Note: keys should be ordered correctly
const views = ref({
  cart: false,
  shippingDetails: false,
  paymentDetails: false
});

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};
const refreshCartItems = async () =>{
  /**
   * Method to refresh cart product items details from backend server.
   */

  // Update the cart items details from backend server.
  await storeCheckout.refreshCartItems(storeEndpoint.cartCheckEndpoint);
};
const checkViewRequirements = async (matchedName='') => {
  /**
   * Method to check path name of current route, if it's not 'cart' then you need to check all required
   * data for the requested view is available.
   */

  // Check if 'matchedName' it's not 'cart' view.
  if(matchedName !== 'cart'){
    // Need to check count of products in the cart and return true or false.
    if(storeCheckout.itemsCount <= 0){
      return false
    }
    // Need to check if current route path name is 'paymentDetails' and the 'shippingDetails' is set or not.
    else return !(matchedName === 'paymentDetails' && !storeCheckout.isShippingDetailsSet);
  }
  else {
    return true
  }
};
const setViews = async (matchedName='') => {
  /**
   * Method to check current route name is exists within 'views', if so, set the existing one and
   * ones before it to be true.
   *
   * @param {String} matchedName The value of path name of current/next route.
   */

  // Initialize a new obj variable.
  // in Javascript, object parameter passed by value by its keys passed by reference, so it's better
  // to clone the obj that you will change its keys.
  let viewsObj = structuredClone(views.value);

  // Reset all the keys value of 'viewsObj' to be as false.
  /*
     Notice: if loop over object, the (key) will represent the 'index' of loop
             while the 'value' of the loop will represent the (value) of that (key).
   */
  for (let key in viewsObj){
    // Set current 'viewsObj' key to be false.
    viewsObj[key] = false;
  }

  // Check that the 'matchedName' is existing with 'viewsObj' keys.
  if(matchedName !== '' && Object.keys(viewsObj).includes(matchedName)){

    // Loop over 'viewsObj'
    for (let key in viewsObj) {

      // Set current views key to be true if fulfills the requirements.
      viewsObj[key] = await checkViewRequirements(key);

      // If current views key is same as 'matchedName', then break the loop and no need to continue.
      if (matchedName === key) {
        break;
      }
    }
  }

  // Set 'viewsObj' to 'views'
  views.value = viewsObj;
};

/*
  call functions
*/
// Set page title.
setPageTitle(`Jamie & Cassie | Checkout`);

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await refreshCartItems();
await setViews(router.currentRoute.value.name).then(() => {
  // if views for 'to.name' is false, replace current route to be 'cart'.
  if (views.value[router.currentRoute.value.name] === false) {
    router.replace({name: 'cart'});
  }
});

/*
  call imported method
*/
onErrorCaptured(() => {
  errMsg.value = "Something went wrong!";
});

// Keep watching the state of 'storeCheckout'
storeCheckout.$subscribe((mutation, state) => {
  // You can specify type of mutation.
  if ( [MutationType.direct].includes(mutation.type) ) {

    // Check that if current cart items count is zero or less and current route path name is not 'cart' OR
    // the current route path name is 'paymentDetails' and all required shipping details is not set yet.
    if (
        (router.currentRoute.value.name !== 'cart' && storeCheckout.itemsCount <= 0 ) ||
        (router.currentRoute.value.name === 'paymentDetails' && storeCheckout.isShippingDetailsSet === false)
    ){
      router.replace({name: 'cart'});
    }
  }
});

</script>

<style scoped>

.bc {
  font-size: 2.1vmin;
  /*font-size: 1.7vmin;*/
  text-transform: uppercase;
  font-weight: 400;
  text-align: center;
  margin: auto;
  padding: 0;
  list-style-type: none;
  /*width: 100%;*/
  max-width: 100%;
  height: 100px;
  counter-reset: breadcrumb;
  position: relative;
}

.bc:before {
  position: absolute;
  top: 21px;
  left: 12.5%;
  content: '';
  width: 75%;
  height: 2px;
  background: #0F1111;
}

.bc .bc_item {
  float: left;
  padding-top: 58px;
  width: 25%;
  position: relative;
}

.bc .bc_item:after {
  font-size: 3.2vmin!important;
  /*font-size: 2.8vmin!important;*/
  counter-increment: breadcrumb;
  content: counter(breadcrumb);
  position: absolute;
  top: 0;
  left: calc(50% - 21px);
  width: 40px;
  height: 40px;
  border: 2px solid #0F1111;
  border-radius: 50%;
  line-height: 35px;
  background: #fff;
  box-shadow: 0 2px 5px 0 rgb(15 17 17 / 50) !important;
}

.bc .bc_complete:after {
  background: #0F1111;
  color: #fff;
}

.bc_item > a{
  color: #0F1111;
  text-decoration: none;
}

.bc_item > a:hover{
  color: rgb(204, 12, 57);
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