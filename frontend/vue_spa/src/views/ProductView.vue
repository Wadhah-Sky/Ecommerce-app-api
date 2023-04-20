<template>

  <section class="section-content padding-y bg-white">
    <div class="container">

      <!-- ============================ COMPONENT 1 ================================= -->
      <div class="card">
        <div class="row no-gutters">

          <product-item-gallery-component :images="storeProduct.selectedProductItem.images"/>

          <product-main-component :store-product="storeProduct"
                                  :title="storeProduct.dataResult.title"
                                  :description="storeProduct.dataResult.summary"
                                  :price-currency-symbol="storeProduct.selectedProductItem.price_currency_symbol"
                                  :list-price-amount="storeProduct.selectedProductItem.list_price_amount"
                                  :deal-price-amount="storeProduct.selectedProductItem.deal_price_amount"
                                  :promotion-title="storeProduct.selectedProductItem.promotion_title"
                                  :promotion-summary="storeProduct.selectedProductItem.promotion_summary"
                                  :trigger-get-data-result="triggerGetDataResult"
          />

        </div> <!-- row.// -->
      </div> <!-- card.// -->
      <!-- ============================ COMPONENT 1 END .// ================================= -->

      <br>

      <product-reviews-component />

    </div> <!-- container .//  -->
  </section>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ProductMainComponent from "@/components/ProductMainComponent";
import ProductItemGalleryComponent from "@/components/ProductItemGalleryComponent";
import ProductReviewsComponent from "@/components/ProductReviewsComponent";
// import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useProductStore} from "@/store/Product";
import {cleanUrlQuery} from "@/common/cleanURL";
import {endpointSerializer} from "@/common/endpointSerializer";
import {useRouter, useRoute} from "vue-router";
import{defineProps} from "vue";

export default {
  name: "ProductView",
  components: {
    ProductMainComponent,
    ProductItemGalleryComponent,
    ProductReviewsComponent,
    // ContentLoaderComponent
  }
};
</script>
<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  productSlug: {
    type: String,
    required: true
  },
  productItemSlug: {
    type: [String, undefined],
    required: false
  },
  productItemAttr: {
    type: [String, undefined],
    required: false
  },
});
const storeEndpoint = useEndpointStore();
const storeProduct = useProductStore();
const router = useRouter();
const route = useRoute();

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};
const triggerGetDataResult = async (method, productSlug, productItemSlug, productItemAttr, onlyItem=false) => {
  /**
   * Trigger the function in the store to retrieve data from backend using a specific endpoint url.
   */

  // Set the endpoint.
  let endpoint = endpointSerializer(
      storeEndpoint.storeProductDetailsEndpoint,
      [productSlug],
      [
          {
            query: 'item_s',
            value: productItemSlug
          },
          {
            query: 'attr',
            value: productItemAttr
          },
          {
            query: 'only_item',
            value: onlyItem
          }
      ]
  );

  // Get the data from backend.
  await storeProduct[method](endpoint);

  // Check if return response is empty or not.
  if(Object.keys(storeProduct.dataResult).length === 0 || Object.keys(storeProduct.selectedProductItem).length === 0){
    await router.replace(
        {
          name: 'page-not-found',
          // preserve current path and remove the first char to avoid the target URL starting with `//`
          params: { pathMatch: route.path.substring(1).split('/') },
          // preserve existing query and hash if any
          query: route.query,
          hash: route.hash
        }
    );
  }
};
const cleanUrl = (registeredArray, queryObj) =>{
  /**
   * Method to clean view url.
   */

  // Call cleanUrlQuery method.
  let cleanedQueryObj = cleanUrlQuery(registeredArray, queryObj);
  if (Object.keys(cleanedQueryObj).length !== Object.keys(queryObj).length) {
    // Note: When trying to replace current router values, set 'name' value not 'path'
    //       because will not work.
    router.replace({
      name: route.name,
      query: cleanedQueryObj
    });
  }
};

/*
  call functions
*/
setPageTitle(`Jamie & Cassie | ${storeProduct.dataResult?.title}`);
cleanUrl(['itemS', 'attr'], route.query);

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await triggerGetDataResult(
    'getDataResult',
    props.productSlug,
    props.productItemSlug,
    props.productItemAttr,
    false
);

// /*
//  Note: 'onBeforeRouteUpdate' guard can be use when trying to update the current route url (path), while
//        'onBeforeRouteLeave' can be use when trying to leave the current route (path) to another route (path).
// */
// onBeforeRouteLeave(()=> {
//   // Reset store filter to default values when trying to leave the store view.
//   storeProduct.$reset();
//
// });

</script>

<style scoped>

</style>