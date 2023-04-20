<template>

  <main class="col-md-6 border-left">
    <article class="content-body">

      <h2 class="title">{{props.title}}</h2>

      <div v-if="props.promotionTitle || props.promotionSummary" class="content h5">
          <span v-if="props.promotionTitle" class="badge bg-danger">{{ props.promotionTitle }}</span>
          <span v-if="props.promotionSummary" class="badge bg-white">{{ props.promotionSummary }}</span>
      </div>

      <div class="mb-3">

          <div v-if="props.dealPriceAmount">
            <span class="price-symbol h6">{{ props.priceCurrencySymbol }}</span>
            <span class="price h4">{{ props.dealPriceAmount }}</span>
            <del class="price-old h5">{{ props.listPriceAmount }}</del>
          </div>

          <div v-else>
            <span class="price-symbol h6">{{ props.priceCurrencySymbol }}</span>
            <span class="price h4">{{ props.listPriceAmount }}</span>
          </div>

        </div>

      <p>{{props.description}}</p>

      <hr>

      <product-select-component :store-product="storeProduct"
                                :trigger-get-data-result="props.triggerGetDataResult"
      />

      <div class="btn btn-add-cart">
        <span class="text me-2">Add to Cart</span>
        <font-awesome-icon icon="fa-solid fa-cart-shopping" />
      </div>

    </article> <!-- product-info-aside .// -->

  </main> <!-- col.// -->


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ProductSelectComponent from "@/components/ProductSelectComponent";
import{toRef, defineProps} from "vue";

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
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  priceCurrencySymbol: {
    type: String,
    required: true
  },
  listPriceAmount: {
    type: [String, Number],
    required: true
  },
  dealPriceAmount: {
    type: [String, Number, undefined],
    required: false
  },
  promotionTitle: {
    type: [String, undefined],
    required: false
  },
  promotionSummary: {
    type: [String, undefined],
    required: false
  },
  triggerGetDataResult:{
    type: Function,
    required: true
  }
});
const storeProduct = toRef(props, 'storeProduct');

</script>

<style scoped>

.title{
  color: #565959 !important;
}

.badge{
  border-radius: 0!important;
}

.bg-white{
  color: rgb(204, 12, 57);
}

.price-symbol, .price{
  color: #B12704 !important;
}

/*.link-title a{*/
/*  color: #0F1111 !important;*/
/*  text-decoration: none;*/
/*}*/
/*.link-title a:hover{*/
/*  text-decoration: underline;*/
/*}*/

.btn-add-cart {
  color: #e9ecef;
  background-color: #0F1111 !important;
  letter-spacing: 1px;
  border-width: 1px;
  border-style: solid;
  border-color: #D5D9D9 !important;
  border-radius: 8px;
  box-shadow: 0 2px 5px 0 rgb(213 217 217 / 50 ) !important;
}

.btn-add-cart:hover {
  cursor: pointer;
  transition: color 200ms ease-in-out;
  background-color: #e9ecef !important;
  color: #0F1111 !important;
}

</style>
