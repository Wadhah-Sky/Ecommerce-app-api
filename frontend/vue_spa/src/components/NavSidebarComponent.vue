<template>

  <sidebar-menu :menu="storeNavSidebar.menu"
                :collapsed="true"
                :showOneChild="true"
  />


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {defineProps, toRef} from 'vue';

export default {
  name: "NavSidebarComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storeNavSidebar: {
    type: Object,
    required: true
  },
});
const storeNavSidebar = toRef(props, 'storeNavSidebar');

</script>

<style scoped>

</style>