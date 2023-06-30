<template>

  <div class="container">
    <div class="content">

      <div class="card">

        <div class="row">

          <div :class="[storeCheckout.itemsCount > 0 ? 'col-md-8' : 'col-md-12', 'cart']">

            <div class="title">
              <div class="row justify-content-between">
                <div class="col-md-9">
                  <h4>
                    <b>Shopping cart</b>
                  </h4>
                </div>
                <div class="col-md-3 align-self-center text-right" style="width: 100px">

                  <span>
                    {{storeCheckout.itemsCount}}
                  </span>
                  <span class="ps-1">
                    {{storeCheckout.itemsCount > 1 ? 'items' : 'item'}}
                  </span>

                </div>
              </div>
            </div>

            <hr>

            <ul class="shopping-cart-items">

              <template v-if="storeCheckout.cartProducts.length > 0">

                <li v-for="(item, index) in storeCheckout.cartProducts" :key="index"
                    class="clearfix pt-2">

                  <div class="row ms-1 me-1 mt-2 ps-0 pe-0" style="width: 100%">

                    <!--This to be consider the frame of image-->
                    <div class="col-md-3 mb-2 pt-2 pb-2 img-container"
                         style="vertical-align: middle;
                              padding-left: 0;
                              padding-right: 0;
                              width: 120px;
                              height: 166px;"
                    >
                      <router-link
                          :to="{name: 'product', params: { slug: item.slug }, query: { itemS: item.itemS }}"
                          style="text-decoration: none"
                      >

                        <img v-lazy="item.thumbnail" :alt="item.title">

                      </router-link>

                    </div>

                    <div class="col-md-9 me-0 ps-0 pe-0">

                      <router-link
                          :to="{name: 'product', params: { slug: item.slug }, query: { itemS: item.itemS }}"
                          class="item-name"
                      >
                        {{ item.title }}
                      </router-link>

                      <div class="row mt-2 row-cols-auto">

                        <template v-for="(val, index) in item.attributes"
                                  :key="index"
                        >

                          <span class="col-4 pe-0 align-self-center"
                              style="display: inherit; font-size: 13px; font-weight: 400;">{{ index }}
                          </span>
                          <span class="col-8 pe-0 align-self-center"
                                style="font-size: 13px;">{{ val }}
                          </span>

                        </template>

                        <template v-if="item.sku">

                          <span class="col-4 pe-0 align-self-center"
                                style="display: inherit; font-size: 13px; font-weight: 400;"
                          >
                            SKU
                          </span>
                          <span class="col-8 pe-0 align-self-center"
                                style="font-size: 13px; font-weight: 400">
                            {{ item.sku }}
                          </span>

                        </template>

                      </div>

                      <div class="row mt-3 justify-content-between">

                        <div class="col-md-4 mb-2 pe-0">
                          <number-input-spinner-component :value="quantity[item.sku]"
                                                          :min="item.limitPerOrder > 0 ? 1 : 0"
                                                          :max="item.limitPerOrder <= 0 ? 0 : item.limitPerOrder"
                                                          :integer-only="true"
                                                          @input="updateItemQuantity(item.sku, $event.currentValue)"
                                                          :disabled="[0, 1].includes(item.limitPerOrder)"
                          />
                        </div>

                        <div class="col-md-8 mb-2 pe-0 item-price">
                          {{ item.currencySymbol }}
                          {{ storeCheckout.itemSubtotal(item.priceAmount, quantity[item.sku]) }}
                        </div>

                      </div>

                    </div>

                  </div>

                  <div class="remove-item"
                       @click="removeItemFromCart(index, item.sku)"
                  >
                    Remove
                  </div>

                </li>

              </template>

              <li v-else>
                <div class="row ms-0 me-0 pt-2 text-center clearfix">
                  <div class="col align-self-center">Cart is empty</div>
                </div>
              </li>

          </ul>

          </div>

          <div v-if="storeCheckout.itemsCount > 0" class="col-md-4 summary">

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

            <div class="pt-4">

              <div class="mb-1">
                <span style="font-weight: 600">
                  Quantity
                </span>
              </div>

              <div class="row row-cols-2 justify-content-between">

                <div class="col">
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

                  <component
                      :is="[undefined, '', null, 0].includes(storeCheckout.cartApiTotalDiscountAmount) ? 'span': 'del'"
                      style="float: right; font-weight: 400"
                  >
                    {{ storeCheckout.cartApiPriceCurrencySymbol }} {{ storeCheckout.cartTotalQuantityPriceAmount }}
                  </component>

                </div>

              </div>

              <form class="mt-3 mb-2" @submit.prevent>

<!--                <div class="mb-1" style="font-weight: 600">Coupon</div>-->
                <div class="row">

                  <div class="col-10 pe-0 me-0 input-wrapper">

                    <label for="coupon" class="mb-1 has-value">Coupon</label>
                    <input v-model="coupon"
                           id="coupon"
                           class="has-value"
                           type="text"
                           placeholder="Enter the code"
                           autocomplete="off"
                           @input="resetCartApiState"
                    >

                  </div>

                  <div class="col-2 ps-0 ms-0" @click="checkCoupon" style="margin-top: 10px">
                    <span>
                      <button>
                        <font-awesome-icon icon="fa-solid fa-arrow-right"/>
                      </button>
                    </span>
                  </div>

                </div>

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

                  <div v-show="![undefined, '', null].includes(storeCheckout.cartApiErrorMsg)"
                       class="row mt-2 me-0 pe-0 alert alert-secondary"
                       role="alert" style="padding: 0; margin: 0"
                  >
                    <div class="col">

                      <span class="alert-msg">{{storeCheckout.cartApiErrorMsg}}</span>

                    </div>

                  </div>

                </div>

              </form>

              <div v-if="![undefined, '', null, 0].includes(storeCheckout.cartApiTotalDiscountAmount)"
                   class="row row-cols-2 justify-content-between mb-3"
              >

                <div class="col">
                  <span
                      style="float: left; font-weight: 400">Total discount</span>
                </div>

                <div class="col align-self-center">
                  <span style="float: right; font-weight: 400;">
                    {{ storeCheckout.cartApiPriceCurrencySymbol }} {{storeCheckout.cartApiTotalDiscountAmount}}
                  </span>
                </div>

              </div>

              <div class="row row-cols-2 justify-content-between">

                <div class="col">
                  <span style="float: left; font-weight: 600">Subtotal</span>
                </div>

                <div class="col align-self-center">
                <span style="float: right; font-weight: 400">
                  {{ storeCheckout.cartApiPriceCurrencySymbol }} {{ storeCheckout.cartTotalQuantityPriceAmountWithDiscount }}
                </span>
                </div>

              </div>

              <div class="mb-4">

                <router-link :to="{name: 'shippingDetails'}"
                             :class="['btn', storeCheckout.dataLoading ? 'disabled' : '']"
                >
                  Next
                </router-link>

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
import NumberInputSpinnerComponent from "@/components/NumberInputSpinnerComponent";
import{ref, onBeforeMount, watch} from "vue";

export default {
  name: "CartView",
  components: {
    NumberInputSpinnerComponent
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const storeEndpoint = useEndpointStore();
const storeCheckout = useCheckoutStore();
// Quantity should be: {<itemSkuValue>: <itemQuantityValue>, ...}
const quantity = ref({});
const coupon = ref(storeCheckout.cartApiCouponCode);

// Define function
const updateItemQuantity = (sku, qty) => {
  /**
   * Update certain item quantity in 'cartProducts' and 'quantity' object.
   */
  quantity.value[sku] = qty;
  storeCheckout.updateItemQuantity(sku, qty)
};
const removeItemFromCart = (index, sku) => {
  /**
   * Remove certain item from cart and all related references.
   */

  // Pop the item out of cart.
  storeCheckout.removeItem(index);

  // Remove the item from quantity reference.
  delete quantity.value[sku];
};
const checkCoupon = async () => {
  /**
   * Method to check coupon value by make an HTTP POST request to backend server.
   */

  // Check that 'coupon' value is set.
  if (![undefined, '', null].includes(coupon.value)) {

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
            "sku": item.sku || "",
            "quantity": quantity.value[item.sku] || ""
          }
      );
    }

    // Create data object.
    let data = {
      "coupon": coupon.value,
      "items": items
    };

    // Trigger cart check method with required parameters.
    await storeCheckout.cartCheck(storeEndpoint.cartCheckEndpoint, data);
  }
}
const resetCartApiState = () => {
  /**
   * Method to reset cart api related states in checkout store.
   */

  // If error msg is null and total price is 0, pass.
  if ([undefined, '', null].includes(storeCheckout.cartApiErrorMsg) &&
      [undefined, '', null, 0].includes(storeCheckout.cartApiTotalPriceAmount)){
    return false
  }
  else {
    storeCheckout.resetCartApiState();
  }
};

// Life-cycle
// Note: since our <template> attributes count on value of quantity, so don't use onMounted() because
//       will trigger after template is mounted.
onBeforeMount(() => {

  // Loop over cart products
  for (let item of storeCheckout.cartProducts){
    // Set value of quantity of each product item, use item 'sku' as key.
    quantity.value[item.sku] = item.quantity;
  }

  // Check coupon code.
  checkCoupon();
});

// watch quantity reference
watch(() => quantity.value, (currentValue, oldValue) =>
    {
      storeCheckout.resetCartApiState();
    },
    {
      deep: true
    }
);

</script>

<style scoped lang="scss">

$main-color: #0F1111;
$light-text: #ABB0BE;

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}

.shopping-cart-items {
  list-style: none;
  padding-top: 8px;
  padding-left: 0;

  li {
    margin-bottom: 18px;
  }

  // if you dont use 'max' with height and width, the image will show as resized (fill).
  // use transform 'scale' to show image in good shape.
  img {
    vertical-align: middle;
    overflow-clip-margin: inherit;
    overflow: clip;
    //transform: scale(0.8);
    max-width: 100%;
    max-height: 100%;
  }

  .item-name {
    color: $main-color;
    text-decoration: none;
    display: block;
    padding-top: 0;
    font-size: 14px;

    text-overflow: ellipsis;
    overflow: hidden;
    display: -webkit-box !important;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    white-space: normal;
  }
  .item-name:hover{
    text-decoration: underline;
  }

  .item-price {
    color: #B12704;
    font-size: 15px;
    font-weight: 400;
  }

  .remove-item {
    margin-right: 26px;
    cursor: pointer;
    float: right;
    color: rgb(204, 12, 57);
    font-size: 14px;
  }
  .remove-item:hover{
    color: $light-text;
  }
}

.lighter-text {
  color: $light-text;
}

.title{
    margin-bottom: 3vh;
}
.card{
    margin: auto;
    /*max-width: 950px;*/
    width: 100%;
    box-shadow: 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    //border-radius: 1rem;
    border: transparent;
}
.cart{
    background-color: #fff;
    padding: 4vh 5vh;
    //border-bottom-left-radius: 1rem;
    //border-top-left-radius: 1rem;
}
.summary{
  color: $main-color;
  background-color: #e9ecef;
  padding: 4vh 5vh;
  //border-top-right-radius: 1rem;
  //border-bottom-right-radius: 1rem;
}
hr{
    margin-top: 2rem;
}

form {
  padding: 2vh 0;

  select {
    border: 1px solid rgba(0, 0, 0, 0.137);
    padding: 1.5vh 1vh;
    margin-bottom: 4vh;
    outline: none;
    width: 100%;
    background-color: rgb(247, 247, 247);
  }

  //input {
  //  //margin: auto;
  //  border: 1px solid rgba(0, 0, 0, 0.137);
  //  border-right: none;
  //  padding: 1.5vh 0 1.5vh 1.5vh;
  //  outline: none;
  //  width: 100%;
  //  background-color: rgb(247, 247, 247);
  //}
  //
  //input:focus::-webkit-input-placeholder {
  //  color: transparent;
  //}

  button{
    width: 100%;
    padding-top: .59rem;
    padding-bottom: .59rem;
    //padding-top: 1.08rem;
    //padding-bottom: 0.16rem;
    border: 1px solid #E5E7EB;
    border-left: none;
    background-color: rgb(247, 247, 247);
    outline: none;
  }
  button:hover .fa-arrow-right{
    transform: translateX(18%);
    color: #464646;
    transition: all 400ms ease-in-out;
  }
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

// Use it with input
//#code {
//  background-image: linear-gradient(
//          to left, rgba(255, 255, 255, 0.253) ,
//          rgba(255, 255, 255, 0.185)),
//          url("https://img.icons8.com/small/16/000000/long-arrow-right.png"
//  );
//  background-repeat: no-repeat;
//  background-position-x: 95%;
//  background-position-y: center;
//}

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

.btn:hover, a.disabled {
  background-color: #e9ecef;
  color: $main-color;
}

a.disabled{
  pointer-events: none;
}

a:active{
  transform: translateY(3%);
  transition: transform 0.2s;
}

.input-wrapper {
  align-items: center;
}

label[for=coupon] {
  width: -moz-max-content;
  width: max-content;
  display: -webkit-box;
  display: -ms-flexbox;
  -webkit-box-align: center;
  -ms-flex-align: center;
  -webkit-box-pack: center;

  pointer-events: none;
  display: block;
  align-items: center;
  justify-content: center;
  webkit-transform-origin: top left;
  transform-origin: top left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  left: .75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5rem;
  color: #0f1111;
  position: relative;
  top: 1.125rem;
  z-index: 2;
  transition: top 0.3s, font-size 0.3s, color 0.3s, transform 0.3s;
}

label.has-value {
  //color: #9e9e9e;
  color: #0f1111;
  -webkit-transform: scale(.8) translateY(-.65em);
  transform: scale(.8) translateY(-.65em);
}

input#coupon {
  padding: 1.08rem 0.75rem 0.16rem 0.75rem;
  font-size: 1rem;
  width: 100%;
  border-radius: 0;
  border: 1px solid #E5E7EB;
  border-right: none;
  outline: 2px solid transparent;
  outline-offset: 2px;
   -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-color: rgb(247, 247, 247);
  margin: -17px 0 0;
  //padding: 24px 10px 10px; //
  color: #0f1111;
  position: relative;
  z-index: 1;
  box-sizing: border-box;
  transition: padding-top 0.3s;
}

input#coupon:focus {
  //border-color: #0f1111;
  outline: none;
}

// for phones and tablets
@media(max-width:767px){
  .card{
    margin: 3vh auto;
  }
  .cart{
    padding: 4vh;
  }
  .img-container{
    margin: auto ;
  }
  .remove-item{
    margin: 0!important;
  }
}

// for big screens
@media(min-width:768px){
  .img-container{
    margin-right: 10px ;
  }
}

</style>