<template>

  <div class="container">
    <div class="content">

      <div class="card">

        <div v-if="!storeCheckout.dataLoading" class="row">

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
                                   @card-name="cardName = $event"
                                   @card-number="cardNumber = $event"
                                   @card-expiry="cardExpiry = $event"
                                   @card-security-code="cardSecurityCode = $event"
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

              <div style="display: inline-block; margin-top: 8px">

                <div v-show="![undefined, '', null].includes(storeCheckout.orderApiErrorMsg)"
                     class="row mt-2 me-0 pe-0 alert alert-secondary"
                     role="alert" style="padding: 0; margin: 0"
                >
                  <div class="col">

                    <span
                        class="alert-msg">{{ storeCheckout.orderApiErrorMsg }}</span>

                  </div>

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

                  <button :class="['btn', storeCheckout.dataLoading ? 'disabled' : '']"
                          @click="setOrder"
                  >
                    Set Order
                  </button>

                </template>

              </div>

            </div>

          </div>

        </div>

        <content-loader-component v-else style="transition: all 0.3s ease-in-out" />

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
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import MazPaymentInfoForm from "@/components/MazPaymentInfoForm";
import {ref} from "vue";

export default {
  name: "CheckoutPaymentView",
  components: {
    ContentLoaderComponent,
    MazPaymentInfoForm
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const storeCheckout = useCheckoutStore();
const storeEndpoint = useEndpointStore();
const cardName = ref(null);
const cardNumber =  ref(null);
const cardExpiry = ref(null);
const cardSecurityCode = ref(null);
const isPaymentInfoFormSet = ref(false);
const isValidPaymentInfoForm = ref(false);

// Define functions
const loadPaymentDetails = async () =>{
  /**
   * Method to trigger checkout functions that related to payment.
   */
  await storeCheckout.getPaymentMethods(storeEndpoint.paymentMethodsEndpoint);
};
const setOrder = async () => {
  /**
   * Method to set data and call backend server in order to set purchase order
   */

  // Initialize an empty list.
  let items = []

  // Loop over cart items.
  // Note: we prefer to loop over cart directly not over 'quantity' variable.
  for (let item of storeCheckout.cartProducts) {
    // Push item certain details as object.
    /*
       Note: since this object will send to backend server as JSON object, so make
             sure so send keys and its values as string with single/double quotes ('')/("").
     */
    items.push(
        {
          "sku": item.sku,
          "quantity": item.quantity
        }
    );
  }

  // Set data variable that will send as JSON object to backend server.
  let data = {
    "coupon": storeCheckout.cartApiCouponCode || null,
    "cart": {
      "items": items
    },
    "shipping": {
      "method": storeCheckout.shippingDetails['shippingMethod'],
      "personal_info": {
        "first_name": storeCheckout.shippingDetails['firstName'],
        "last_name": storeCheckout.shippingDetails['lastName'],
        "email": storeCheckout.shippingDetails['email'],
        "phone_number": storeCheckout.shippingDetails['phoneNumber']
      },
      "country": {
        "iso_code": storeCheckout.shippingDetails['country']
      },
      "address_details": {
        "address1": storeCheckout.shippingDetails['address1'],
        "address2": storeCheckout.shippingDetails['address2'],
        "region": storeCheckout.shippingDetails['region'],
        "city": storeCheckout.shippingDetails['city'],
        "postal_code": storeCheckout.shippingDetails['postalCode']
      }
    },
    "payment": {
      "method": storeCheckout.paymentDetails['paymentMethod'],
      "card_details": {
        "cardholder_name": cardName.value,
        "card_number": cardNumber.value,
        "card_expiry": cardExpiry.value,
        "card_ccv": cardSecurityCode.value
      },
      "use_shipping_address": storeCheckout.paymentDetails['useShippingAddress'] || false,
      "billing": {
        "personal_info": {
          "first_name": storeCheckout.paymentDetails['firstName'],
          "last_name": storeCheckout.paymentDetails['lastName'],
          "phone_number": storeCheckout.paymentDetails['phoneNumber']
        },
        "country": {
          "iso_code": storeCheckout.paymentDetails['country'],
        },
        "address_details": {
          "address1": storeCheckout.paymentDetails['address1'],
          "address2": storeCheckout.paymentDetails['address2'],
          "region": storeCheckout.paymentDetails['region'],
          "city": storeCheckout.paymentDetails['city'],
          "postal_code": storeCheckout.paymentDetails['postalCode']
        }
      }
    }
  };

  // Trigger set purchase order method with required parameters.
  await storeCheckout.setPurchaseOrder(storeEndpoint.OrderCreateEndpoint, data);
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