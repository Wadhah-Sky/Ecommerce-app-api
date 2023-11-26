<template>

  <div class="container">
    <div class="content">

      <div class="card">

        <div class="row">

          <div class="col-md-8 customer-info">

            <div class="title">
              <div class="row justify-content-between">
                <div class="col-md-12">
                  <h4>
                    <b>Shipping info</b>
                  </h4>
                </div>
              </div>
            </div>

            <hr>

            <maz-details-info-form :details="storeCheckout.shippingDetails"
                                   :set-details-method="storeCheckout.setShippingDetails"
                                   :countries="storeCheckout.countries"
                                   @is-valid="isValidInfoForm = $event"
                                   @is-required-set="isInfoFormSet = $event"
            />

          </div>

          <div class="col-md-4 shipping">

            <div class="title">
              <div class="row">
                <div class="col-md-12">
                  <h4>
                    <b>Shipping</b>
                  </h4>
                </div>
              </div>
            </div>

            <hr>

            <div class="pt-4 mb-1">

              <maz-select label="Shipping method"
                          class="shipping-method"
                          type="text"
                          v-model="shippingMethod"
                          ref="shippingMethodInput"
                          :options="storeCheckout.shippingMethods"
                          color="black"
                          required
                          no-radius
                          @update:model-value="storeCheckout.setShippingDetails('shippingMethod', String($event).trim())"
              />

              <div style="display: inline-block; margin-top: 8px">

                <div v-if="storeCheckout.dataLoading"
                     style="margin-bottom: 5px"
                >
                  <font-awesome-icon :icon="['fa-solid', 'spinner']"
                                     style="color: #0f1111; font-size: 15px;"
                                     spin
                  />
                  Loading
                </div>

                <div v-show="![undefined, '', null].includes(storeCheckout.shippingApiErrorMsg)"
                     class="row mt-2 me-0 pe-0 alert alert-secondary"
                     role="alert" style="padding: 0; margin: 0"
                >
                  <div class="col">

                    <span class="alert-msg">{{ storeCheckout.shippingApiErrorMsg }}</span>

                  </div>

                </div>

              </div>

              <template v-if="storeCheckout.isShippingInfoSet">

                <div class="row row-cols-2 justify-content-between ps-1 pe-1">

                  <div class="col">
                    <span style="float: left; font-weight: 600">Cost</span>
                  </div>

                  <div class="col align-self-center">
                  <span style="float: right; font-weight: 400">
                    {{storeCheckout.shippingApiPriceCurrencySymbol}} {{storeCheckout.shippingApiCostPriceAmount}}
                  </span>
                  </div>

                </div>

              </template>

              <div class="mb-4">

                <template v-if="isInfoFormSet === false ||
                                (shippingMethodInput.required && [undefined, null, ''].includes(shippingMethod)) ||
                                ![undefined, '', null].includes(storeCheckout.shippingApiErrorMsg)"
                >
                  <span class="btn disabled">
                    Set required* fields
                  </span>
                </template>

                <template v-else-if="isValidInfoForm === false">
                  <span class="btn disabled">
                    Set valid inputs
                  </span>
                </template>

                <template v-else>
                  <router-link :to="{name: 'checkoutPayment'}"
                               :class="['btn', storeCheckout.dataLoading ? 'disabled' : '']"
                  >
                    Next
                  </router-link>
                </template>

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useCheckoutStore} from "@/store/Checkout";
import { MutationType } from 'pinia';
import MazDetailsInfoForm from "@/components/MazDetailsInfoForm";
import {ref} from "vue";

export default {
  name: "CheckoutShippingView",
  components: {
    MazDetailsInfoForm
  }
}
</script>

<script setup>
/*
  Define handlers (properties, props and computed)
*/
const storeCheckout = useCheckoutStore();
const storeEndpoint = useEndpointStore();
const shippingMethod = ref(null);
const shippingMethodInput = ref(null);
const isValidInfoForm = ref(false);
const isInfoFormSet = ref(false);
// keys in to watch if changed in 'storeCheckout'.
const keys = ['shippingMethod', 'country', 'region', 'city', 'postalCode'];
let timer;

// Define functions
const calculateShippingCost = async () => {
  /**
   * Method to get shipping cost by make an HTTP POST request to backend server.
   */

  // Create data object.
  /*
     Note: since this object will send to backend server as JSON object, so make
           sure so send keys and its values as string with single/double quotes ('')/("").
   */
  let data = {
    "method": shippingMethod.value,
    "country": {
      "iso_code": storeCheckout.shippingCostCheckDetails['country_iso_code']
    },
    "address_details": {
      "region": storeCheckout.shippingCostCheckDetails['region'],
      "city": storeCheckout.shippingCostCheckDetails['city'],
      "postal_code": storeCheckout.shippingCostCheckDetails['postal_code']
    }
  };

  // Trigger shipping cost method with required parameters.
  await storeCheckout.shippingCost(storeEndpoint.shippingCostEndpoint, data);
};
const loadShippingDetails = async () =>{
  /**
   * Method to trigger checkout functions that related to shipping.
   */
  await storeCheckout.getCounties(storeEndpoint.shippingCountiesEndpoint);
  await storeCheckout.getShippingMethods(storeEndpoint.shippingMethodsEndpoint);
  await storeCheckout.setShippingMethod();

  // Set value of shipping method if it's exist in the store.
  if(storeCheckout.shippingDetails['shippingMethod']){
   shippingMethod.value = storeCheckout.shippingDetails['shippingMethod'] || null;
  }

  if(storeCheckout.isShippingInfoSet && shippingMethod.value !== null){
   await calculateShippingCost();
  }
};

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await loadShippingDetails();

// Keep watching the state of 'storeCheckout'
storeCheckout.$subscribe((mutation, state) => {
  // You can specify type of mutation.
  if ( [MutationType.direct].includes(mutation.type) ) {
    // Check if current mutation events key is included within the defined 'keys' list to watch.
    // Note: we want that to Trigger calculate shipping cost method only if (shipping method,
    //       country, region, city and postal code) inputs value is changed in the store, also if
    //       all required shipping info have set.
    if (keys.includes(mutation.events.key) && storeCheckout.isShippingInfoSet){
      // Clear timer, in case its set.
      clearTimeout(timer);
      // Set timer.
      timer = setTimeout(() => {calculateShippingCost();},2000);
    }
  }
});

// Watch shipping method
// watch(() => shippingMethod.value, (currentValue, oldValue) =>
//     {
//       calculateShippingCost();
//     },
//     {
//       immediate: true,
//       lazy: true
//     }
// );


</script>

<style lang="scss" scoped>

$main-color: #0F1111;

.card{
    margin: auto;
    /*max-width: 950px;*/
    width: 100%;
    box-shadow: 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    //border-radius: 1rem;
    border: transparent;
}

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}

.customer-info{
    background-color: #fff;
    padding: 4vh 5vh;
}

.title{
    margin-bottom: 3vh;
}

.shipping{
  color: $main-color;
  background-color: #e9ecef;
  padding: 4vh 5vh;
  //border-top-right-radius: 1rem;
  //border-bottom-right-radius: 1rem;
}

hr{
    margin-top: 2rem;
}

label{
  font-weight: 400;
  color: $main-color;
}

label, option {
  font-size: 14px;
}
input::placeholder {
  font-size: 13px;
}

.btn {
  text-decoration: none;
  background-color: $main-color;
  border-color: $main-color;
  color: #fff;
  width: 100%;
  font-size: 1.1rem;
  margin-top: 4vh;
  padding: 1.5vh;
  border-radius: 3px;
}

.btn:focus {
  box-shadow: none;
  outline: none;
  color: white;
  -webkit-box-shadow: none;
  -webkit-user-select: none;
  transition: none;
}

.btn:hover, .btn.disabled {
  background-color: #e9ecef;
  color: $main-color;
  border-color: $main-color;
}

a.disabled{
  pointer-events: none!important;
}

a:active{
  transform: translateY(3%);
  transition: transform 0.2s;
}

.alert-secondary{
  opacity: 80%;
  background-color: #e9ecef;
  transition: all 0.3s ease;
}

.alert-msg{
  display: inline-block;
  margin: auto;
  color: rgb(204, 12, 57);
  font-size: 14px;
  font-weight: 400;
  text-align: center;
}

// for phones and tablets
@media(max-width:767px){
  .card{
    margin: 3vh auto;
  }
  .customer-info{
    padding: 4vh;
  }
  .related-field{
    padding-left: 0!important;
  }
  input::placeholder {
    font-size: 12px;
  }
}
// for big screens
@media(min-width:768px){
  .related-field{
    padding-left: 10px!important;
  }
}
</style>