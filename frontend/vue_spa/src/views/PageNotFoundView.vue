<template>
  <div class="container mt-3">
    <h1 class="not-found"> {{ message }}</h1>
  </div>
</template>

<script>

/*
  Libraries, methods, properties and components imports
*/
import {ref} from 'vue';

export default {
  name: "PageNotFoundView"
}

</script>

<script setup>

/*
  Define handlers (constants, props and computed)
*/
const message = ref("404 - Not Found!");

/*
  Define functions
*/
const setPageTitle = async (title) => {
  /**
   * set a given title string as the webpage title.
   */
  // async make the function return a promise when it's done.
  return document.title = title;
};

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
// await makes the function wait for a promise.
await setPageTitle('Jamie & Cassie | 404 - Requested page not found');

</script>

<style>
.not-found {
  color: red;
  text-align: center;
}
</style>