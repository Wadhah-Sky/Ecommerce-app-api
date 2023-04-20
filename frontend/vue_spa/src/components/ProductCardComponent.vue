<template>

  <figure class="card card-product-grid">

    <router-link
        :to="{
          name: 'product',
          params: { productSlug: props.productSlug },
          query: { itemS: props.productItemSlug, attr: props.productItemAttr }
        }"
        class="img-wrap"
    >
      <img v-lazy="props.thumbnail" :alt="props.productTitle">
    </router-link>

    <figcaption class="card-body info-wrap">

      <div class="content">

        <div class="row justify-content-between">

          <div class="col-9">

            <h6 v-if="productItemsCount > 1">

              <span class="badge text-bg-secondary"
                    style="
                      background-color: #e9ecef !important;
                      color: #0F1111 !important;
                      cursor: default;
                    "
                    v-tooltip
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Multi variations of the product"
              >Multi variations
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
              params: {productSlug: props.productSlug},
              query: {itemS: props.productItemSlug, attr: props.productItemAttr}
            }"
            class="title"
        >
          <span v-tooltip
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                :title="props.productTitle.length > 87 ? props.productTitle : ''"
          >{{ props.productTitle }}</span>
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
import {defineProps} from "vue";

export default {
  name: "ProductCardComponent"
}
</script>

<script setup>

const props = defineProps({
  productSlug: {
    type: String,
    required: true
  },
  productItemSlug: {
    type: String,
    required: true
  },
  productItemAttr: {
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
  rating: {
    type: [String, Number, undefined],
    required: false
  },

});

</script>

<style scoped>

.badge{
  border-radius: 0!important;
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
</style>