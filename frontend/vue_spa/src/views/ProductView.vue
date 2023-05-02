<template>

  <section class="section-content padding-y bg-white">
    <div class="container">

      <template v-if="!updateData">
        <!-- ============================ COMPONENT 1 ================================= -->
        <div class="card">
          <div class="row no-gutters">

            <template v-if="storeProduct.selectedProductItem.images">

              <product-item-gallery-component :images="storeProduct.selectedProductItem.images"/>

            </template>

            <template v-if="Object.keys(storeProduct.dataResult).length > 0">

              <product-main-component :store-product="storeProduct"
                                      :slug="props.slug"
                                      :title="storeProduct.dataResult.title"
                                      :summary="storeProduct.dataResult.summary"
                                      :price-currency-symbol="storeProduct.selectedProductItem.price_currency_symbol"
                                      :list-price-amount="storeProduct.selectedProductItem.list_price_amount"
                                      :deal-price-amount="storeProduct.selectedProductItem.deal_price_amount"
                                      :promotion-title="storeProduct.selectedProductItem.promotion_title"
                                      :promotion-summary="storeProduct.selectedProductItem.promotion_summary"
                                      :low-stock="storeProduct.selectedProductItem.low_stock"
                                      :temporarily-not-available="storeProduct.selectedProductItem.temporarily_not_available"
                                      :trigger-get-data-result="triggerGetDataResult"
              />

            </template>


          </div> <!-- row.// -->
        </div> <!-- card.// -->
        <!-- ============================ COMPONENT 1 END .// ================================= -->

        <!-- ============================ COMPONENT 2 ================================= -->

        <template v-if="Object.keys(storeProduct.productDetails)?.length > 0">

          <br>

          <product-details-component title="Product Details"
                                     :details="storeProduct.productDetails"/>

        </template>

        <!-- ============================ COMPONENT 2 END .// ================================= -->

        <!-- ============================ COMPONENT 3 ================================= -->

        <template v-if="Object.keys(storeProduct.productAdditionalDetails)?.length > 0">

          <br>

          <product-details-component title="Additional Details"
                                     :details="storeProduct.productAdditionalDetails"/>

        </template>

        <!-- ============================ COMPONENT 3 END .// ================================= -->

        <!-- ============================ COMPONENT 4 ================================= -->

        <template v-if="storeProduct.dataResult['related_products']?.length > 0">

          <br>

          <section class="section-name">

            <product-swiper-component slider-title="Related products"
                                      :products="storeProduct.dataResult['related_products']"
            />

          </section>


        </template>

        <!-- ============================ COMPONENT 4 END .// ================================= -->

        <br>
        <!-- ============================ COMPONENT 5 ================================= -->

        <product-reviews-component/>
        <!-- ============================ COMPONENT 5 END .// ================================= -->

      </template>

      <template v-else>
        <content-loader-component style="transition: all 0.3s ease-in-out" />
      </template>

    </div> <!-- container .//  -->
  </section>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useProductStore} from "@/store/Product";
import ProductMainComponent from "@/components/ProductMainComponent";
import ProductItemGalleryComponent from "@/components/ProductItemGalleryComponent";
import ProductReviewsComponent from "@/components/ProductReviewsComponent";
import ProductDetailsComponent from "@/components/ProductDetailsComponent";
import ProductSwiperComponent from "@/components/ProductSwiperComponent";
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import {cleanUrlQuery} from "@/common/cleanURL";
import {endpointSerializer} from "@/common/endpointSerializer";
import {useRouter, useRoute, onBeforeRouteUpdate, onBeforeRouteLeave} from "vue-router";
import{defineProps, ref} from "vue";

export default {
  name: "ProductView",
  components: {
    ProductMainComponent,
    ProductItemGalleryComponent,
    ProductReviewsComponent,
    ProductDetailsComponent,
    ProductSwiperComponent,
    ContentLoaderComponent
  }
};
</script>
<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  // product slug.
  slug: {
    type: String,
    required: true
  },
  // product item slug.
  itemS: {
    type: [String, undefined],
    required: false,
    default: ''
  },
  // product item attributes.
  // attr: {
  //   type: [String, undefined],
  //   required: false
  // },
});
const router = useRouter();
const route = useRoute();
const storeEndpoint = useEndpointStore();
const storeProduct = useProductStore();
const updateData = ref(false);

/*
  Note: 'onBeforeRouteUpdate' guard can be use when trying to update the current route url (path), while
        'onBeforeRouteLeave' can be use when trying to leave the current route (path) to another route (path).

        Both of them should be at top of setup().
 */
onBeforeRouteUpdate(async (to, from, next) => {

  if (from.params.slug !== to.params.slug){
    // In case trying to view another slug in this view.
    updateData.value = true;

    // Trigger the method that retrieve the data from backend with new parameters.
    await triggerGetDataResult(
        'getDataResult',
        to.params.slug,
        to.query.itemS,
        null,
        false
    );

    updateData.value = false;
  }
  next();

});

onBeforeRouteLeave(()=> {
  // Reset store filter to default values when trying to leave the store view.
  storeProduct.$reset();
  // stop watching

});

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};
const triggerGetDataResult = async (method, slug, itemS, attr=null, onlyItem=false) => {
  /**
   * Trigger the function in the store to retrieve data from backend using a specific endpoint url.
   */

  // Note: 'itemS' is can't be null even if you are using 'attr' query parameter due in case that
  //       the product item don't had any attribute, so we need to use its slug.

  // Set the endpoint.
  let endpoint = endpointSerializer(
      storeEndpoint.storeProductDetailsEndpoint,
      [slug],
      [
          {
            query: 'item_s',
            value: itemS
          },
          {
            query: 'attr',
            value: attr
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
    await router?.replace(
        {
          name: 'page-not-found',
          // preserve current path and remove the first char to avoid the target URL starting with `//`
          params: { pathMatch: route?.path.substring(1).split('/') },
          // preserve existing query and hash if any
          query: route?.query,
          hash: route?.hash
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
    router?.replace({
      name: route?.name,
      query: cleanedQueryObj
    });
  }
};

/*
  call functions
*/
setPageTitle(`Jamie & Cassie | ${storeProduct.dataResult?.title}`);
if( route ){
  /*
   Info: Somtimes when press back button in the browser, happen to raise the below error:

         typeError: Cannot read properties of undefined (reading 'query')

         So we check that route is exists (not null or undefined) and has 'query' object
         as property before run cleanUrl method.
   */
  cleanUrl(['itemS'], route?.query);
}

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
// Error: caught (in promise) TypeError: Cannot read properties of null (reading 'scope')

await triggerGetDataResult(
    'getDataResult',
    props.slug,
    props.itemS,
    null,
    false
);

</script>

<style scoped>

</style>