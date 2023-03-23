<template>


  <!-- ========================= SECTION CONTENT ========================= -->

    <section class="section-content padding-y">

      <div class="container">

        <deals-departments-component :data="departmentsArray" :slug="props.slug" />
        <deals-main-component :store-pagination="storePagination" />

      </div> <!-- container .//  -->

    </section>
    <!-- ========================= SECTION CONTENT END// ========================= -->

</template>

<script>
import DealsDepartmentsComponent from "@/components/DealsDepartmentsComponent";
import DealsMainComponent from "@/components/DealsMainComponent";
import {usePaginationStore} from "@/store/Pagination";
import {useEndpointStore} from "@/store/StaticEndpoint";
import {axios} from "@/common/api.axios";
import { onBeforeRouteUpdate} from "vue-router";
import {ref} from 'vue';

export default {
  name: "DealsView",
  components: {
    DealsDepartmentsComponent,
    DealsMainComponent
  }
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
  page: {
    type: String,
    required: true
  }
});
const storePagination = usePaginationStore();
const storeEndpoint = useEndpointStore();
// const route = useRoute();
// const router = useRouter();
const departmentsArray = ref([]);

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};
const setStorePaginationPageNumber = (page) => {
  /**
   * Set the 'page' value from url query string to 'pageNumber' in the storePagination.
   * */

  storePagination.pageNumber = page;
};
const getDealsDepartments = async () => {
  /**
   * Function to retrieve all Departments of the store from backend server.
   */

  let endpoint = storeEndpoint.storeDepartmentsEndpoint;
  try {
    const response = await axios.get(endpoint);
    departmentsArray.value = response.data;
  } catch (error) {
    console.log("Error while trying to retrieve the requested data from backend server!");
  }
};
const triggerGetProductsDataResult = async (slug, page) => {
  /**
   * Trigger the 'getDataResult' function in the store using a specific endpoint url.
   */

  let endpoint = '';

  // in case slug and page is not empty, zero or false.
  if (slug && page){
    // Set the page number in the store pagination.
    setStorePaginationPageNumber(page);

    endpoint = storeEndpoint.storeProductsOffersEndpoint + `${slug}/`;
    await storePagination.getDataResult(endpoint + (`?page=${page}`));
    // if (!storePagination.dataResult.length){
    //   await router.replace(
    //     {
    //       name: 'page-not-found',
    //       // preserve current path and remove the first char to avoid the target URL starting with `//`
    //       params: { pathMatch: route.path.substring(1).split('/') },
    //       // preserve existing query and hash if any
    //       query: route.query,
    //       hash: route.hash
    //     }
    //     );
    // }
  }
};

/*
  call functions
*/
// Set page title.
setPageTitle("Jamie & Cassie | Latest deals");

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await getDealsDepartments();
await triggerGetProductsDataResult(props.slug, props.page);

/*
 Note: 'onBeforeRouteUpdate' guard can be use when trying to update the current route url (path), while
       'onBeforeRouteLeave' can be use when trying to leave the current route (path) to another route (path).
*/
onBeforeRouteUpdate(async (to, from, next) => {
  await triggerGetProductsDataResult(to.params.slug, to.query.page);
  next();
});


</script>

<style scoped>

</style>