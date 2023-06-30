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
                    <b>Payment info</b>
                  </h4>
                </div>
              </div>
            </div>

            <hr>

            <maz-payment-info-form :payment-details="storeCheckout.paymentDetails"
                                   :set-payment-details="storeCheckout.setPaymentDetails"
                                   :is-payment-card="storeCheckout.isPaymentCard"
                                   :payment-methods="storeCheckout.paymentMethods"
                                   :countries-endpoint="storeEndpoint.shippingCountiesEndpoint"
                                   @is-valid="isValidPaymentInfoForm = $event"
                                   @is-required-set="isPaymentInfoFormSet = $event"
            />

          </div>

          <div class="col-md-4 shipping">

            <div class="title">
              <div class="row">
                <div class="col-md-12">
                  <h4>
                    <b>Summary</b>
                  </h4>
                </div>
              </div>
            </div>

            <hr>

            <div class="pt-4 mb-1">

              <div class="row row-cols-2 justify-content-between mb-3">

                <div class="col">
                  <span style="float: left; font-weight: 600">Cart</span>
                </div>

                <div class="col align-self-center" >
                  <span style="float: right; font-weight: 400">

                    <span>
                      {{storeCheckout.itemsCount}}
                    </span>

                    <span class="ps-1">
                      {{ +storeCheckout.itemsCount > 1 ? 'items' : 'item' }}
                    </span>

                  </span>
                </div>

              </div>

              <div class="mb-1">
                <span style="font-weight: 600">
                  Quantity
                </span>
              </div>

              <div class="row row-cols-2 justify-content-between mb-3">

                <div class="col" >
                  <span style="float: left">

                    <span>
                      {{ storeCheckout.cartTotalQuantity }}
                    </span>

                    <span class="ps-1">
                      {{ +storeCheckout.cartTotalQuantity > 1 ? 'items' : 'item' }}
                    </span>

                  </span>
                </div>

                <div class="col align-self-center">

                  <component :is="[undefined, '', null, 0].includes(storeCheckout.cartApiTotalDiscountAmount) ? 'span': 'del'"
                             style="float: right; font-weight: 400"
                  >
                    {{ storeCheckout.cartApiPriceCurrencySymbol }} {{ storeCheckout.cartTotalQuantityPriceAmount }}
                  </component>

                </div>

              </div>

              <div v-if="![undefined, '', null, 0].includes(storeCheckout.cartApiTotalDiscountAmount)"
                   class="row row-cols-2 justify-content-between mb-3"
              >
                <div class="col">
                  <span style="float: left; font-weight: 400">Total discount</span>
                </div>

                <div class="col align-self-center">
                  <span style="float: right; font-weight: 400;">
                    {{storeCheckout.cartApiPriceCurrencySymbol}} {{ storeCheckout.cartApiTotalDiscountAmount }}
                  </span>
                </div>

              </div>

              <div class="row row-cols-2 justify-content-between mb-3">

                <div class="col">
                  <span style="float: left; font-weight: 400">Shipping</span>
                </div>

                <div class="col align-self-center">
                  <span style="float: right; font-weight: 400">
                    {{storeCheckout.shippingApiPriceCurrencySymbol}} {{ storeCheckout.shippingApiCostPriceAmount }}
                  </span>
                </div>

              </div>

              <div class="row row-cols-2 justify-content-between mb-3">

                <div class="col">
                  <span style="float: left; font-weight: 600">Grand total</span>
                </div>

                <div class="col align-self-center">
                  <span style="float: right; font-weight: 400">
                    {{storeCheckout.cartApiPriceCurrencySymbol}} {{ storeCheckout.checkoutGrandTotalPriceAmount }}
                  </span>
                </div>

              </div>

              <div class="mb-5">

                <template v-if="isPaymentInfoFormSet === false">

                  <span class="btn disabled">
                    Set required* fields
                  </span>

                </template>

                <template v-else-if="isValidPaymentInfoForm === false">

                  <span class="btn disabled">
                    Set valid inputs
                  </span>

                </template>

                <template v-else>

                  <router-link :to="{name: 'paymentDetails'}"
                               :class="['btn', storeCheckout.dataLoading ? 'disabled' : '']"
                  >
                    Set order
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
import mazPaymentInfoForm from "@/components/MazPaymentInfoForm";
import {ref} from "vue";

export default {
  name: "PaymentDetailsView",
  components: {
    mazPaymentInfoForm
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const storeCheckout = useCheckoutStore();
const storeEndpoint = useEndpointStore();
const isPaymentInfoFormSet = ref(false);
const isValidPaymentInfoForm = ref(false);

// Define functions
const loadPaymentDetails = async () =>{
  /**
   * Method to trigger checkout functions that related to payment.
   */
  await storeCheckout.getPaymentMethods(storeEndpoint.paymentMethodsEndpoint);
};

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await loadPaymentDetails();

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

.customer-info-details{
  list-style: none;
  padding-top: 8px;
  padding-left: 0;
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
  pointer-events: none;
}

// This will effect all Maz input in parent and children components
.m-input-wrapper{
  border-radius: 0!important;
}

.shipping-method .m-input-wrapper-input,
.shipping-method .m-input-wrapper-right,
.shipping-method .m-select-list{
  background-color: rgb(247, 247, 247)!important;
  outline: none;
}

.shipping-method .m-select-list{
  background-color: rgb(247, 247, 247)!important;
  outline: none;
  width: 100%!important;
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