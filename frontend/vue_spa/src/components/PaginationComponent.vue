<template>

  <nav class="mt-4" aria-label="Page navigation sample">
    <ul class="pagination justify-content-center">
      <li :class="['page-item', isDisabledPrev(1) ]"
          :tabindex="isDisabledPrev(1) === 'disabled' ? -1 : 0"
      >
        <router-link
            :to="{ path: route.path, query: { ...route.query, page: pageNumber - 1 } }"
            class="page-link"
        >
          <span> Previous </span>
        </router-link>
      </li>

      <li v-show="!range.includes(1)" class="page-item disabled"
          :tabindex="-1">
        <span class="page-link"> ... </span>
      </li>


      <router-link v-for="( page, index ) in range" :key="index"
                   :to="{ path: route.path, query: { ...route.query, page: page } }"
                   v-slot="{ href, navigate, isActive, isExactActive }"
                   custom
      >

        <li class="page-item" :class="[ href === route.fullPath ? 'active' : '']"
            :tabindex="href === route.fullPath ? -1 : 0"
        >

          <a class="page-link"
             :href="href"
             :class="[isActive ? 'router-link-active' : '', isExactActive ? 'router-link-exact-active' : '']"
             @click="navigate"
             :style="[ href === route.fullPath ? {pointerEvents: 'none', display: 'inline-block'} : '']"
          >
            {{ page }}
          </a>

        </li>

      </router-link>


<!--      <li v-for="( page, index ) in range" :key="index"-->
<!--          class="page-item"-->
<!--          :class="[isActive(page)]"-->

<!--      >-->
<!--        <router-link :to="{ path: route.path, query: { ...route.query, page: page } }"-->
<!--                     class="page-link"-->
<!--                     @click="changePage(page)"-->

<!--        >-->
<!--          <span> {{ page }} </span>-->
<!--        </router-link>-->
<!--      </li>-->

      <li v-show="!range.includes(pagesCount)"
          class="page-item disabled"
          :tabindex="-1">
        <span class="page-link"> ... </span>
      </li>

      <li :class="['page-item', isDisabledNext(pagesCount)]"
          :tabindex="isDisabledNext(pagesCount) === 'disabled' ? -1 : 0">
        <router-link
            :to="{ path: route.path, query: { ...route.query, page: pageNumber + 1 } }"
            class="page-link"
            >
          <span> Next </span>
        </router-link>
      </li>
    </ul>
  </nav>

</template>

<script>

/*
* Note: <router-link/> when is active will create <a> tag with attribute aria-current=<value> depending of the type:
*       Type: 'page' | 'step' | 'location' | 'date' | 'time' | 'true' | 'false' (string)
*       so when trying to use 'ref' attribute with <router-link/>, use the appropriate one of the value above,
*       which is class to apply on the rendered <a> when the link is exact active.
*       'aria-current' attribute can be used to identify or visually style an element among a set of related items.
*/

/* replace parameter within :to directive of <router-link> acts like router.push, the only difference
*  is that it navigates without pushing a new history entry which means the user when click on
*  back button in browser will not return him back to last entry, as its name suggests - it
*  replaces the current entry.
*/

/*
  Libraries, methods, variables and components imports
*/
import {useRoute} from "vue-router";
import {defineProps, ref} from "vue";

export default {
  name: "PaginationComponent"
}

</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  range: {
    type: Array,
    required: true
  },
  pageNumber: {
    type: [String, Number],
    required: true
  },
  pagesCount: {
    type: [Function, Number],
    required: true
  }
});
const range = ref(props.range);
const pageNumber = ref(+props.pageNumber);
const pagesCount = ref(+props.pagesCount);
// route: represent current url in the browser.
const route = useRoute();

// const computedPageNum = computed({
//   get: () => props.pageNumber,
//   set: (val) => (props.pageNumber + val)
// });

/*
  Define functions
*/
// const changePage = async (page) => {
//   /**
//    * Function that check and change current active page's link to new one, when click on the link,
//    * be aware the function 'changePageNumber' will trigger the 'getDataResult' in the store.
//    */
//
//    /*
//     Change page in store using new page number and trigger the 'getDataResult' function in store.
//     Note: since we are using vue router navigation guard we don't need to push to the new url
//           of clicked <router-link> because <router-link> has 'navigation' function which will
//           trigger by default and will make sure to update the url and history state, you can
//           ban this default behavior using @click.capture.prevent with the <router-link> or with
//           any other element that wrapped by <router-link custom>.
//           Don't forget we are using navigation guard to trigger this function 'changePage' when
//           the url of current view is updated, e.g. like when update value of page query parameter.
//    */
//   await storePagination.value.changePage(<backendEndpoint>, page);
//
//   //#####################################################################
//   // The below code is for learning purpose.
//
//   /*
//     How to update url in the browser without actually push to that url?
//     Note: this will not update the history or Vue Router and not recommended.
//    */
//
//   /* 1- Make a variable of read-only property 'window.location' that returns a Location object
//         with information about the current location of the document.
//    */
//   // const url = new URL(window.location);
//
//   /* 2- The set() method of the URLSearchParams interface sets the value associated with a given
//         search parameter to the given value. If there were several matching values, this method
//         deletes the others. If the search parameter doesn't exist, this method creates it.
//    */
//   // url.searchParams.set('page', page);
//
//   // OR you can set url pathname manually as shown below.
//   // url.pathname = `${route.path}?page=${page}`;
//
//   /* 3- Update the 'page' query parameter silently using history.pushState() method that adds
//         an entry to the browser's session history stack, Note: we will update the current state.
//    */
//   // let myState = history.state
//   // myState.back = route.fullPath
//   // myState.current = route.path + `?page=${page}`
//   // router.currentRoute.value.query.page = page
//   // myState.replaced = true
//   // history.pushState({...history.state, myState}, '', url);
//
//   /*
//     How to force Vue Router to push to the route (url) when you click on <router-link> and trigger
//     this function in case you are using @click.capture.prevent ?
//    */
//
//   // route.query.page = page
//   // router.push(Object.assign(route.query.page, {page: page}))
//
//   /*
//      How to update the url in the browser using Vue Router?
//      Note: the Vue Router will render automatically the view using this new url if the new :key value
//            that set to the <div> element which hold the <component> in <router-view> inside App.vue and
//            this value we can set it to be route.fullPath (in order to destroy the view and re-render it
//            whenever the full path changed) or use route.path (the same thing whenever the path changed) or
//            we can Not set the :key (in this case Vue router only re-render the view whenever we travel
//            between views), so if this value is different from the current :key for current
//            <div :key="?"><component/></div> value will destroy the view and re-render it again.
//    */
//
//   // router.push({path: route.path, query: {...route.query, page: page} });
//
// };

const isDisabledPrev = (page) => {
  /**
   * Function to check whether the current pageNumber in store is equal or less than sent value.
   * if so, return 'disable'.
   */
  return +pageNumber.value <= +page ? 'disabled' : '' ;
};
const isDisabledNext = (page) => {
  /**
   * Function to check whether the current pageNumber in store is equal or bigger than sent value.
   * if so, return 'disable'.
   */
  return +pageNumber.value >= +page ? 'disabled' : '' ;
};

/*
  call functions
*/

</script>

<style scoped >


</style>