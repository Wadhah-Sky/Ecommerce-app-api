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
import {useNavSidebarStore} from "@/store/NavSidebar";

export default {
  name: "NavSidebarComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const storeNavSidebar = useNavSidebarStore();

</script>

<style scoped>

</style>