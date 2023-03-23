<template>

  <header>

    <form class="filter">

      <div class="row mb-5">

        <div v-show="storeFiltering.dataResult['Brand']" class="row mb-3">

          <div class="row">

            <div class="filter-group-label">

              <span>Brand</span>

            </div>

          </div>

          <div class="row row-cols-auto">

            <div v-for="brand in storeFiltering.dataResult['Brand']" :key="brand" class="col">

              <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="brands"
                       :id="brand.brand_name"
                       :checked="storeFiltering.dataResult['Brand'].length <= 1"
                       :disabled="storeFiltering.dataResult['Brand'].length <= 1"
                       :value="brand.brand_name">
                <span class="btn btn-white-dark">{{brand.brand_name}}</span>
              </label>

            </div>

          </div>

        </div>

        <div v-show="storeFiltering.dataResult['Size']" class="row mb-3">

          <div class="row">

            <div class="filter-group-label">

              <span>Size</span>

            </div>

          </div>

          <div class="row row-cols-auto">

            <div v-for="size in storeFiltering.dataResult['Size']" :key="size" class="col">

              <label class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       :id="size.size_name"
                       :checked="storeFiltering.dataResult['Size'].length <= 1"
                       :disabled="storeFiltering.dataResult['Size'].length <= 1"
                       :value="size.size_name">
                <span class="btn btn-white-dark">{{size.size_name}}</span>
              </label>

            </div>

          </div>

        </div>

      </div>

    </form>

  </header>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {useFilteringStore} from "@/store/Filter";
import {usePaginationStore} from "@/store/Pagination";
import {useEndpointStore} from "@/store/StaticEndpoint";
import {useRoute} from "vue-router";
import {watch, ref, defineProps} from "vue";

export default {
  name: "TopFilterComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  departmentName: {
    type: String,
    required: false
  },
  categoryName: {
    type: String,
    required: false
  },
  typeName: {
    type: String,
    required: false
  }
});
const storeFiltering = useFilteringStore();
const storePagination = usePaginationStore();
const storeEndpoint = useEndpointStore();
const route = useRoute();
const brands = ref([]);
/* the simplified way to:

 const propsSet = (props.departmentName && props.categoryName && props.typeName) ? true : false

 is:

 const propsSet = !!(props.departmentName && props.categoryName && props.typeName)
*/
const propsSet = !!(props.departmentName && props.categoryName && props.typeName);

watch( () => [...brands.value], (currentValue, oldValue) => {

  let endpoint = '';
  // console.log(route.query.page)
  route.query.page = 1;

  if (propsSet){
    endpoint = storeEndpoint.storeProductsEndpoint +
        (`${props.departmentName}/${props.categoryName}/${props.typeName}/?brand=${brands.value}`);
  }
  else {
    endpoint = storeEndpoint.storeProductsEndpoint + (`?brand=${brands.value}`);
  }
  storePagination.changePageNumber(1,endpoint + '&page=1' );
  console.log(endpoint + (`&page=${storePagination.pageNumber}`))

});

// const triggerGetDataResult = async () => {
//   /**
//    *
//    */
//   // await storePagination.getDataResult();
// }

</script>

<style scoped>

</style>