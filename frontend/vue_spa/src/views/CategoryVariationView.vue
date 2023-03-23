<template>

  <section class="section-name padding-y-sm">
    <div class="container">

      <header class="section-heading">
        <h4 class="section-title">{{ data['node'] }}</h4>
      </header><!-- sect-heading -->

      <div class="row">

        <div v-for="( category, index ) in data['leaf_nodes']" :key="index" class="pt-4 col-sm-3">

          <div class="a-button-div">

            <router-link
                :to="{
                    name: 'categoryStore',
                    params: { slug: category['slug'], subSlug: 'all' }
                }"
                class="a-button">
                <span> {{ category['title'] }} </span>
            </router-link>

          </div>

        </div>

      </div>

    </div><!-- container // -->
  </section>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {defineProps, ref} from "vue";
import { axios } from "@/common/api.axios.js";
import router from "@/router";
import {useRoute} from "vue-router";
import {useEndpointStore} from "@/store/StaticEndpoint";

export default {
  name: "CategoryVariationView"
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
  }
});
const storeEndpoint = useEndpointStore();
const data = ref({});
const route = useRoute();

/*
  Define functions storeHomepageBannersURL
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};
const getCategoryVariationList = async () => {
  /**
   * Get the categories' variation list from backend server for the selected department.
   */

  /*
   join static URL with its parameter using concat() method.
   Note: The downside of using concat() is that you must be certain that 'str1' (first argument) is a string.
         You can pass non-string parameters to concat(), but you will get a TypeError if str == null.
  */
  let endpoint = storeEndpoint.storeCategoriesEndpoint.concat(`${props.slug}/`);
  const response = await axios.get(endpoint)
  data.value = response.data[0]
  if (data.value.length === 0) {
    /*
      In case the getDataResult() returned a response with status code 404 or 200 (with empty result),
      we need to make sure to replace the current component before its rendered (while in setup life cycle)
      with another component (like page-not-found), be careful that you should REPLACE not PUSH to the
      'page-not-found' component because whenever you do a router.push() you add new route record into
      routing stack and if you tried to move back by pressing on back button in the browser will move
      you back to the component that you actually pushed from which will push you again to 'page-not-found'
      component again and so on while router.replace() will replace the current route record with another one.
    */
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

/*
  call functions
*/

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await getCategoryVariationList();

/*
  Set page title
*/
setPageTitle(`Jamie & Cassie | ${data.value['title']} | Categories`);


</script>

<style scoped>

</style>