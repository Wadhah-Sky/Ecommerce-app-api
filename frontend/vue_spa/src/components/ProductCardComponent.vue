<template>

  <figure class="card card-product-grid">

    <router-link
        :to="{
          name: 'product',
          params: { slug: props.slug },
          query: { itemS: props.itemS }
        }"
        class="img-wrap"
    >
      <img v-lazy="props.thumbnail" :alt="props.productTitle" width="260" height="220">
    </router-link>

    <figcaption class="card-body info-wrap">

      <div class="content">

        <div class="row justify-content-between">

          <div class="col-9">

            <h6 v-if="productItemsCount > 1">

              <span class="badge text-bg-secondary available-variation"
                    v-tooltip
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="This product has multi variations"
              >
                Multi {{product_items_variation_string()}}
              </span>

            </h6>

          </div>

          <div class="col-3">

            <h6 v-if="props.rating">

              <span class="badge bg-white" style="color: #0F1111 !important;">4.5
                <font-awesome-icon icon="fa-solid fa-star"/>
              </span>

            </h6>

          </div>

        </div>

      </div>

      <div class="fix-height">
        <div v-if="props.promotionTitle || props.promotionSummary" class="content">
          <span v-if="props.promotionTitle" class="badge bg-danger promotion-title">{{ props.promotionTitle }}</span>
          <span v-if="props.promotionSummary" class="badge bg-white promotion-summary">{{ props.promotionSummary }}</span>
        </div>

        <router-link
            :to="{
              name: 'product',
              params: { slug: props.slug },
              query: { itemS: props.itemS }
            }"
            class="title"
        >
          <span v-tooltip
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                :title="props.productTitle.length > 87 ? props.productTitle : ''"
          >
            {{ props.productTitle }}
          </span>
        </router-link>

        <div class="price-wrap mt-2">

          <div v-if="props.dealPriceAmount">
            <span class="price-symbol">{{ props.priceCurrencySymbol }}</span>
            <span class="price">{{ props.dealPriceAmount }}</span>
            <del class="price-old">{{ props.listPriceAmount }}</del>
          </div>

          <div v-else>
            <span class="price-symbol">{{ props.priceCurrencySymbol }}</span>
            <span class="price">{{ props.listPriceAmount }}</span>
          </div>

        </div> <!-- price-wrap.// -->
      </div>

    </figcaption>

  </figure>


</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
// import {useRouter} from "vue-router";
import {defineProps} from "vue";

export default {
  name: "ProductCardComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  slug: {
    type: String,
    required: true
  },
  itemS: {
    type: String,
    required: true
  },
  attr: {
    type: String,
    required: true
  },
  thumbnail: {
    type: String,
    required: true
  },
  productTitle: {
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
  productItemsCount: {
    type: [String, Number, undefined],
    required: false
  },
  productItemsVariation: {
    type: Array,
    // Object or array defaults must be returned from a factory function.
    // The function receives the raw props received by the component as the argument.
    default(rawProps) {
      return []
    }
  },
  rating: {
    type: [String, Number, undefined],
    required: false
  },

});
// const router = useRouter();

/*
  Define functions
*/
const product_items_variation_string = () => {
  /**
   * Convert product_items_variation into a string
   */

  // Check in case there no 'productItemsVariation' passed.
  if (props.productItemsVariation.length === 0){
   return 'variations';
  }
  else{
    // Return string of given array and make sure the last seperator (,) is
    // convert to and word.
    return props.productItemsVariation.join(', ').replace(/,(?!.*,)/gmi, ' and').toLowerCase();
  }
};

// const showProductView = async (slug, itemS) => {
//   /**
//    * Method to push new router state and show new component while recerve the
//    * current state and component, for full example visit:
//    *
//    * https://github.com/vuejs/router/blob/main/packages/router/e2e/modal/index
//    */
//
//   // add backgroundView state to the location, so we can render a different view from this one
//   const backgroundView = router.currentRoute.value.fullPath
//
//   await router.push({
//     name: 'product',
//     params: {slug: slug},
//     query: {itemS: itemS},
//     state: {backgroundView}
//   })
// };

</script>

<style scoped>

.badge{
  border-radius: 0!important;
}

.available-variation {
  background-color: #e9ecef !important;
  color: #0F1111 !important;
  cursor: default;
  text-overflow: ellipsis;
  overflow: hidden;
  /*max-width: 180px;*/
  display: inline-block;
  white-space: nowrap;
}

.promotion-title{
  text-overflow:ellipsis;
  overflow:hidden;
  max-width: 92px;
  display: inline-block;
  white-space: nowrap;
}

.promotion-summary{
  text-overflow:ellipsis;
  overflow:hidden;
  /*max-width: 139px;*/
  display: inline-block;
  white-space: nowrap;
}

.fa-star{
  color: orange;
  filter: drop-shadow(0 0 4px);
}

@media only screen and (max-width: 992px) {
  .available-variation{
    max-width: 120px;
  }
}

@media only screen and (min-width: 993px) {
  .available-variation{
    max-width: 220px;
  }
}
</style>