<template>

  <section class="section-content bg-white">
    <div class="container">

      <div class="row mt-4 mb-0 me-0" style="width: 100%">

        <div class="col-sm-2 col-md-2 col-lg-1 me-0 pe-0">
          <h5>Search:</h5>
        </div>

        <div class="col-sm-9 col-md-9 col-lg-10 me-0 pe-0 text-truncate" >
          <span style="font-size: 16px; text-align: left">{{props.query}}</span>
        </div>
      </div>

    </div>
  </section>

  <!-- ========================= SECTION CONTENT ========================= -->

  <section class="section-content mt-3">

    <div class="container">

      <div class="row pt-3">

        <main v-if="!storePagination.dataLoading" class="col-md-12">

          <header class="border-bottom mb-3 ms-0 pb-2">
            <div class="row row-cols-auto">

              <div class="col">
                <span>
                  {{storePagination.dataCount}} {{ storePagination.dataCount > 1 ? 'items' : 'item' }} found
                </span>

              </div>

            </div>

          </header><!-- sect-heading -->

          <template v-if="storePagination.dataResult.length > 0">

            <div class="row">

              <div v-for="( product, index ) in storePagination.dataResult"
                   :key="index"
                   class="col-12 col-sm-6 col-md-3 col-lg-3 col-xl-3 col-xxl-2"
              >

                <product-card-component :product-title="product.title"
                                        :product-items-count="product.product_items_count"
                                        :rating="product.rating"
                                        :slug="product.slug"
                                        :item-s="product.product_item.slug"
                                        :attr="product.product_item.attributes.join()"
                                        :thumbnail="product.product_item.thumbnail"
                                        :price-currency-symbol="product.product_item.price_currency_symbol"
                                        :list-price-amount="product.product_item.list_price_amount"
                                        :deal-price-amount="product.product_item.deal_price_amount"
                                        :promotion-title="product.product_item.promotion_title"
                                        :promotion-summary="product.product_item.promotion_summary"
                />

              </div> <!-- col.// -->


            </div> <!-- row end.// -->

            <pagination-component :range="storePagination.range"
                                  :page-number="storePagination.pageNumber"
                                  :pages-count="storePagination.pagesCount"
            />

          </template>

          <template v-else>

            <no-result-found-component/>

          </template>

        </main> <!-- col.// -->

        <content-loader-component v-else
                                  style="transition: all 0.3s ease-in-out"
        />

      </div>


    </div> <!-- container .//  -->

  </section>
  <!-- ========================= SECTION CONTENT END// ========================= -->


</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import {useEndpointStore} from "@/store/StaticEndpoint";
import {usePaginationStore} from "@/store/Pagination";
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import NoResultFoundComponent from "@/components/NoResultFoundComponent";
import PaginationComponent from "@/components/PaginationComponent";
import ProductCardComponent from "@/components/ProductCardComponent";
import {cleanUrlQuery} from "@/common/cleanURL";
import {endpointSerializer} from "@/common/endpointSerializer";
import {useRoute, useRouter, onBeforeRouteLeave, onBeforeRouteUpdate} from "vue-router";
import {defineProps} from "vue";

export default {
  name: "StoreSearchView",
  components: {
    ContentLoaderComponent,
    NoResultFoundComponent,
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
  query: {
    type: String,
    required: true
  },
  page: {
    type: String,
    required: true
  }
});
const storeEndpoint = useEndpointStore();
const storePagination = usePaginationStore();
const router = useRouter();
const route = useRoute();

/*
 Note: 'onBeforeRouteUpdate' guard can be use when trying to update the current route url (path), while
       'onBeforeRouteLeave' can be use when trying to leave the current route (path) to another route (path).

       Both of them should be at top of setup().
*/
onBeforeRouteUpdate(async (to, from, next) => {
  await triggerGetProductsDataResult(
      to.params.query,
      to.query.page
  );
  next();
});
onBeforeRouteLeave(()=> {
  storePagination.$reset();
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
const setStorePaginationState = (page) => {
  /**
   * Set the state of the storePagination.
   * */

  /*
    To change (mutate) state of any element in the store, you can do it
    'directly' or using $patch object or $patch as method for complex mutate like
    remove, push and splice.
    Note: mutate using 'patch' have benefit of let subscribe() method to get
          notify that a change is happened in store and so no need to use watch().
   */
  // Mutate directly.
  //storePagination.pageNumber = page;

  // Mutate with $patch function.
  storePagination.$patch((state) =>{
    state.pageNumber= page
  });
};
const triggerGetProductsDataResult = async (query, page) => {
  /**
   * Trigger the 'getDataResult' function in the store using a specific endpoint url.
   */

  // Set the page number in the store pagination.
  setStorePaginationState(page);

  // Set the endpoint.
  let endpoint = endpointSerializer(
      storeEndpoint.storeSearchEndpoint,
      [query],
      [
          {
            query: 'page',
            value: page
          }
      ]
  );

  // Get the data from backend.
  await storePagination.getDataResult(endpoint);
};

/*
  call functions
*/
setPageTitle(`Jamie & Cassie | Search in store`);
cleanUrl(['page'], route.query);

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await triggerGetProductsDataResult(props.query, props.page);

</script>

<style lang="scss" scoped>
// Customize the number of grid tiers of bootstrap

// override the default min-width value (576px) of .col-sm-* column to be 330px
// also you should set the of max-width to same column as breakpoint to .col-md-* which by default it's 768px
@media (min-width: 330px) and (max-width: 767px) {
  .col-sm-6 {
    flex: 0 0 auto;
    width: 50%;
  }
}

</style>