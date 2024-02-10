<template>

  <section class="section-content bg-white">
    <bread-crumbs-component
        v-if="categoryChildrenArray.ancestor_nodes"
        :data="categoryChildrenArray.ancestor_nodes"
    />
  </section>


  <filter-side-panel-component ref="filterComponent"
                               :store-filter="storeFilter"
                               :endpoint="storeEndpoint.storeAttributesEndpoint"
                               :slug="props.slug"
  />

  <!-- ========================= SECTION CONTENT ========================= -->

  <section class="section-content mt-3">

    <div class="container">

      <template v-if="!updateData">
        <store-category-menu-component
            v-if="categoryChildrenArray.leaf_nodes"
            :data="categoryChildrenArray.leaf_nodes"
            :slug="props.slug"
        />
        <store-main-component :store-pagination="storePagination"
                              :store-filter="storeFilter"
                              @toggleFilterSidePanel="filterComponent.triggerToggleSidePanel()"
        />
      </template>

      <template v-else>
        <content-loader-component style="transition: all 0.3s ease-in-out"/>
      </template>


    </div> <!-- container .//  -->

  </section>
  <!-- ========================= SECTION CONTENT END// ========================= -->

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useFilterStore} from "@/store/Filter";
import {usePaginationStore} from "@/store/Pagination";
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import StoreCategoryMenuComponent from "@/components/StoreCategoryMenuComponent";
import StoreMainComponent from "@/components/StoreMainComponent";
import FilterSidePanelComponent from "@/components/FilterSidePanelComponent";
import BreadCrumbsComponent from "@/components/BreadCrumbsComponent";
import { MutationType } from 'pinia';
import {ref, defineProps} from "vue";
import {endpointSerializer} from "@/common/endpointSerializer";
import {cleanUrlQuery} from "@/common/cleanURL";
import {useRoute, useRouter, onBeforeRouteUpdate, onBeforeRouteLeave} from "vue-router";
import {axios} from "@/common/api.axios";

export default {
  name: "StoreCategoryView",
  components: {
    StoreCategoryMenuComponent,
    StoreMainComponent,
    FilterSidePanelComponent,
    BreadCrumbsComponent,
    ContentLoaderComponent
  }
};

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
  page: {
    type: String,
    required: true
  },
  attr: {
    type: [String, undefined],
    required: false,
    default: ''
  },
  minPrice: {
    type: [String, undefined],
    required: false,
    default: ''
  },
  maxPrice: {
    type: [String, undefined],
    required: false,
    default: ''
  },
  selectBy: {
    type: [String, undefined],
    required: false,
    default: ''
  }
});
// Note: inject() for examples stores can only be used inside setup() or functional components.
const router = useRouter();
const route = useRoute();
const storeEndpoint = useEndpointStore();
const storeFilter = useFilterStore();
const storePagination = usePaginationStore();
const filterComponent = ref();
const categoryChildrenArray = ref([]);
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

    // Reset the dataResult of storeFilter using patch function.
    storeFilter.$patch((state) => {
      state.response = {};
    });

    // Get category children.
    await getCategoryChildren(to.params.slug);

    // In case the storeFilter.collapsed is true which means filter
    // component is opened, trigger 'triggerGetDataResult'.
    if (storeFilter.collapsed) {
      await filterComponent.value.triggerGetDataResult(
          storeEndpoint.storeAttributesEndpoint + `${to.params.slug}/`
      );
    }
  }

  await triggerGetProductsDataResult(
      to.params.slug,
      to.query.attr,
      to.query.minPrice,
      to.query.maxPrice,
      to.query.selectBy,
      to.query.page
  );
  updateData.value = false;
  next();
});

onBeforeRouteLeave(()=> {
  // Reset store filter to default values when trying to leave the store view.
  storeFilter.$reset();
  storePagination.$reset();

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
const setStoreFilterState = (attr, minPrice, maxPrice, selectByObjValue) => {
  /**
   * Set the state of filter store.
   * */

  // In case attr is not null, empty or undefined, Set the checked options in the store filter as array.
  let attrOptions = (attr) ? attr.split(',') : [];

  // Initialize an null variable..
  let selectByOption = null
  let availableSelectByOptions = storeFilter.availableSelectByOptions;

  /*
   Get the index of object in 'availableSelectByOptions' array in store filter by
   providing the value of object in mentioned array.
  */
  // Note: use map() method to loop over array of objects, and select specific key
  //       in that object, then find the object index using indexOf() for specific value.
  const index = availableSelectByOptions.map(object => object.value).indexOf(selectByObjValue);

  // Check the indexOf() returned a match or not.
  if(index !== -1){
    // Set selectBy option from available related options in store using index.
    selectByOption = availableSelectByOptions[index];
  }

  // Mutate with $patch function.
  storeFilter.$patch((state) =>{
    state.checkedOptions = attrOptions;
    state.price['minPrice'] = minPrice;
    state.price['maxPrice'] = maxPrice;
    state.selectByOption = selectByOption;
  });
};
const getCategoryChildren = async (slug) => {
  /**
   * Function to retrieve all types of specific category from backend server.
   */

  let endpoint = storeEndpoint.storeCategoryDetailsEndpoint + `${slug}/`;

  try {
    const response = await axios.get(endpoint);
    categoryChildrenArray.value = response.data;
  } catch (error) {
    categoryChildrenArray.value = [];
    // console.log("Error while trying to retrieve the requested data from backend server!");
  }
};
const triggerGetProductsDataResult = async (slug, attr, minPrice, maxPrice, selectByObjValue, page) => {
  /**
   * Trigger the 'getDataResult' function in the store using a specific endpoint url.
   */

  // Set the page number in the store pagination.
  setStorePaginationState(page);

  // Set filter options in store filter.
  setStoreFilterState(attr, minPrice, maxPrice, selectByObjValue);

  // Set the endpoint.
  let endpoint = endpointSerializer(
      storeEndpoint.storeProductsEndpoint,
      [slug],
      [
          {
            query: 'attr',
            value: attr
          },
          {
            query: 'min_price',
            value: minPrice
          },
          {
            query: 'max_price',
            value: maxPrice
          },
          {
            query: 'select_by',
            value: selectByObjValue
          },
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
setPageTitle(`Jamie & Cassie | Store`);
cleanUrl(['attr', 'minPrice', 'maxPrice', 'selectBy', 'page'], route.query);

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await getCategoryChildren(props.slug);
await triggerGetProductsDataResult(
    props.slug,
    props.attr,
    props.minPrice,
    props.maxPrice,
    props.selectBy,
    props.page
);

/*
  Keep watching the state of 'storeFilter' and other stores so whenever there is change in
  the state made by another component will make sure to be reflected over the component or the
  view that use that store.

  Note: You can track a certain state property or all properties.

  Info: 1- it will track the change in state of the store only if it's happened using 'direct', 'patch' object
           or $patch function to change the state.
        2- subscribe working in two ways, means if this component cause or tigger anything that will
           lead to change the state of store by other components (like in parent component), will trigger
           mutation type ('direct', 'patchObject' or 'patchFunction') depending on how you are changing the
           state in parent component, then this component will receive that mutation type.

  Important: be careful, the mutation cause by this component should not use as condition to update
             your data, because this will lead to loop.
 */
storeFilter.$subscribe((mutation, state) => {
  let queryObj = {};
  // You can specify type of mutation.
  // Note: maybe you wonder why we didn't change route.query.<attribute> directly with new values, it won't work.
  if ( [MutationType.patchObject].includes(mutation.type) ) {

    if(storeFilter.checkedOptions.length > 0){
      queryObj['attr'] = storeFilter.checkedOptions.join();
    }
    if(storeFilter.selectByOption !== null){
      queryObj['selectBy'] = storeFilter.selectByOption.value;
    }
    if(!['', null].includes(storeFilter.price['minPrice'])){
      queryObj['minPrice'] = storeFilter.price.minPrice;
    }
    if(!['', null].includes(storeFilter.price['maxPrice'])){
      queryObj['maxPrice'] = storeFilter.price.maxPrice;
    }

    queryObj['page'] = 1;
    // Push new router state.
    router.push(
        {
          path: route.path,
          query: queryObj
        }
    );
  }

  // You can persist the whole state to the local storage whenever it changes.
  // localStorage.setItem('checkedOptions', JSON.stringify(state));

});

// Info: We disabled this part of code, because it's cause to replace router state after we make
//       any push within related component.
// Watch 'route.query' (info: all query's keys are stored as array)
// Note: if you are trying to watch one object, don't but it inside an array [].
// watch(() => route.query, (currentValue, oldValue) =>
//     {
//       // Note: When trying to replace current router values, set 'name' value not 'path'
//       //       because will not work.
//       // router.replace({
//       //   name: route.name,
//       //   query: cleanUrlQuery(Object.keys(props), currentValue)
//       // });
//     },
//     {
//       // By default, watch the callback (its logic) won't be called until the watched source has changed,
//       // here we want to run it at the time of route enter.
//       immediate: true,
//       // Watch the keys of array of 'route.query'.
//       deep: true
//     }
// );

</script>

<style scoped>

</style>