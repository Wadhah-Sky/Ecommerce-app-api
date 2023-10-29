<template>

  <main class="col-md-6 border-left">
    <article class="content-body">

      <h2 class="title">{{props.title}}</h2>

      <div v-if="props.promotionTitle || props.promotionSummary" class="content h5">
          <span v-if="props.promotionTitle" class="badge bg-danger promotion-title">{{ props.promotionTitle }}</span>
          <span v-if="props.promotionSummary" class="badge bg-white promotion-summary">{{ props.promotionSummary }}</span>
      </div>

      <div class="mt-2 mb-3">

          <div v-if="props.dealPriceAmount">
            <span class="price-symbol">{{ props.priceCurrencySymbol }}</span>
            <span class="price">{{ props.dealPriceAmount }}</span>
            <del class="price-old">{{ props.listPriceAmount }}</del>
          </div>

          <div v-else>
            <span class="price-symbol">{{ props.priceCurrencySymbol }}</span>
            <span class="price">{{ props.listPriceAmount }}</span>
          </div>

        </div>

      <p>{{props.summary}}</p>

      <hr>

      <div class="mb-1" style="display: block">
        <span class="me-2" style="font-weight: 400">SKU:</span>
        <span>{{storeProduct.selectedProductItem['sku']}}</span>
      </div>

      <product-select-component :product-options="storeProduct.productOptions"
                                :data-loading="storeProduct.dataLoading"
                                :selected-options="storeProduct.selectedProductItemOptions"
                                :selected-same-option-status="storeProduct.selectedProductItemSameOptionsStatus"
                                :product-options-combination="storeProduct.productOptionsCombination"
                                :product-items-slugs="storeProduct.productItemsSlugs"
                                :use-color-shape="storeProduct.dataResult['use_item_attribute_color_shape']"
                                :use-img="storeProduct.dataResult['use_item_attribute_img']"
                                :trigger-get-data-result="props.triggerGetDataResult"
                                @active-option="activeOption = $event.status"
      />

      <div v-if="props.lowStock || props.temporarilyNotAvailable" class="row mb-2">
        <span style="color: rgb(204, 12, 57); font-weight: 400; transition: all 0.3s ease-in-out">
          {{setStockNote()}}
        </span>
      </div>

      <template v-if="!props.temporarilyNotAvailable">

        <template v-if="storeCheckout.isItemExist(storeProduct.selectedProductItem['slug']) === true">

          <div class="row" style="padding: 0;margin: 0">

            <div class="btn disabled-btn-add-cart">

              <span class="text me-2">Added to Cart</span>
              <font-awesome-icon icon="fa-solid fa-cart-shopping" style="color: #56B544!important;"/>

            </div>

          </div>

        </template>

        <template v-else>

          <div class="row" style="padding: 0;margin: 0" @click="addToCart">

            <div :class="['btn', !activeOption || storeProduct.dataLoading ? 'disabled-btn-add-cart' : 'btn-add-cart']">

              <template v-if="!activeOption || storeProduct.dataLoading">

                <span style="color: #464646; font-weight: 400; transition: all 0.3s ease-in-out">Select from above</span>

              </template>

              <template v-else>

                <span class="text me-2">Add to Cart</span>
                <font-awesome-icon icon="fa-solid fa-cart-shopping"/>

              </template>

            </div>

          </div>

        </template>

      </template>


    </article> <!-- product-info-aside .// -->

  </main> <!-- col.// -->


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {useCheckoutStore} from "@/store/Checkout";
import ProductSelectComponent from "@/components/ProductSelectComponent";
import{toRef, defineProps, ref} from "vue";

export default {
  name: "ProductMainComponent",
  components: {
    ProductSelectComponent
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/

const props = defineProps({
  storeProduct: {
    type: Object,
    required: true
  },
  slug: {
    // product slug
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  summary: {
    type: String,
    required: true
  },
  priceCurrencySymbol: {
    type: String,
    required: true
  },
  listPriceAmount:{
    type: [String, Number],
    required: true
  },
  dealPriceAmount:{
    type: [String, Number],
    required: false
  },
  promotionTitle: {
    type: String,
    required: false
  },
  promotionSummary: {
    type: String,
    required: false
  },
  triggerGetDataResult:{
    type: Function,
    required: true
  },
  lowStock: {
    type: Boolean,
    required: false
  },
  temporarilyNotAvailable: {
    type: Boolean,
    required: false
  }
});
const storeProduct = toRef(props, 'storeProduct');
const storeCheckout = useCheckoutStore();
const activeOption = ref(false);

/*
  Define functions
*/
const setStockNote = () =>{
  /**
   * Method to return certain message depending on variables.
   */
  if (props.lowStock === true){
    return 'Just a few in stock';
  }
  else if (props.temporarilyNotAvailable === true) {
    return  'Temporarily not available';
  }
};
const addToCart = () =>{
  /**
   * Tigger the related method in cart store to add a new item.
   */

  // Check if 'activeOption' is true.
  if (activeOption.value) {

    // Get the current selected product item from product store.
    let item = storeProduct.value.selectedProductItem;

    // Initialize an empty object to store item attributes.
    let attributes = {};

    // Loop over product options.
    for (let [index, val] of Object.entries(storeProduct.value.productOptions)){

      // check that the current array of attributes is contains more than one element.
      if(val.length > 1){
        // Set current 'index' as key in 'attributes' and ite value is a string of joined
        // selected item attributes for current index.
        attributes[index] = item['attributes'][index].join(', ');
      }
    }

    // Set the price amount of item.
    let itemPriceAmount = ['', null, undefined, 0].includes(item['deal_price_amount']) ?
        item['list_price_amount'] : item['deal_price_amount'];

    // Set the object to add into 'products' in cart store.
    let obj = {
      slug: props.slug,
      title: props.title,
      attributes: attributes,
      sku: item['sku'],
      itemS: item['slug'],
      currencySymbol: item['price_currency_symbol'],
      priceAmount: itemPriceAmount,
      limitPerOrder: item['limit_per_order'],
      thumbnail: item['thumbnail'],
      supplierUUID: item['supplier']['uuid'],
      quantity: 1
    };

    // Trigger checkout store 'addItem' with a given value.
    storeCheckout.addItem(obj);
  }
};

</script>

<style scoped>

.title{
  color: #565959 !important;
}

.badge{
  font-size: 14px!important;
  border-radius: 0!important;
}

.bg-white{
  color: rgb(204, 12, 57);
}

.price-symbol, .price{
  color: #B12704 !important;
}

.price-symbol{
  font-size: 13px!important;
}
.price{
  font-size: 18px!important;
}
.price-old{
  font-size: 16px!important;
}

/*.link-title a{*/
/*  color: #0F1111 !important;*/
/*  text-decoration: none;*/
/*}*/
/*.link-title a:hover{*/
/*  text-decoration: underline;*/
/*}*/

.btn-add-cart, .disabled-btn-add-cart {
  margin-top: 8px!important;
  padding: 9px 0 9px 0 !important;
  letter-spacing: 1px;
  border-width: 1px;
  border-style: solid;
  border-color: #D5D9D9 !important;
  border-radius: 0;
  box-shadow: 0 2px 5px 0 rgb(213 217 217 / 50 ) !important;
  transition: all 400ms ease-in-out;
}

.btn-add-cart{
  color: #e9ecef !important;
  background-color: #0F1111 !important;
}

.disabled-btn-add-cart{
  color: #464646 !important;
  background-color: #e9ecef !important;
}

.disabled-btn-add-cart:hover{
  cursor: not-allowed;
}

.btn-add-cart:hover {
  cursor: pointer;
  transition: color 200ms ease-in-out;
  background-color: #e9ecef !important;
  color: #0F1111 !important;
}

.btn-add-cart:active{
  transform: translateY(3%);
  transition: transform 0.2s;
}

.promotion-title{
  margin-right: 6px;
}

.promotion-summary{
  padding-left: 0;
  margin-left: 0;
}

@media only screen and (max-width: 700px) {
  .title{
    font-size: 17px;
  }
  .badge{
    font-size: 13px!important;
  }
}

</style>
