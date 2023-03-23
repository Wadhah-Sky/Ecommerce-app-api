<template>

    <div class="row">
    <main v-if="!storePagination.dataLoading" class="col-md-12" >
        <header class="border-bottom mb-4 pb-3">
          <div class="row row-cols-auto">

              <div class="col" style="padding-right: 0">
                <span>
                  {{ storePagination.dataCount }} {{ storePagination.dataCount > 1 ? 'items' : 'item' }} found
                </span>

              </div>

          </div>
        </header><!-- sect-heading -->

      <div class="row">

        <div v-for="( product, index ) in storePagination.dataResult"
             :key="index"
             class="col-md-3"
        >
          <product-card-component :thumbnail="product.thumbnail"
                                  :product_name="product.product_name"
                                  :product_headline="product.product_headline"
                                  :price_currency="product.price_currency"
                                  :list_price="product.list_price"
                                  :deal_price="product.deal_price"
                                  :offer_info="product.offer_info"
                                  :offer_name="product.offer_name"
          />

        </div> <!-- col.// -->

      </div> <!-- row end.// -->

      <pagination-component :store-pagination="props.storePagination"/>

    </main> <!-- col.// -->

    <content-loader-component v-else style="transition: all 0.3s ease-in-out" />

  </div>


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import PaginationComponent from "@/components/PaginationComponent";
import ProductCardComponent from "@/components/ProductCardComponent";
import {defineProps} from "vue";

export default {
  name: "DealsMainComponent",
  components: {
    ContentLoaderComponent,
    PaginationComponent,
    ProductCardComponent
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storePagination: {
    type: Object,
    required: true
  }
});

</script>

<style scoped>

</style>