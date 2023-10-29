<template>

  <sidebar-menu :menu="storeNavSidebar.menu"
                :collapsed="storeNavSidebar.collapsed"
                :showOneChild="true"
                @update:collapsed="onToggleCollapse"
  />


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {ref, defineProps, toRef, onMounted, onUnmounted, watch} from 'vue';

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
// To get device width use, ref(screen.width)
const windowWidth = ref(window.innerWidth)
// To get device height use, ref(screen.height)
const windowHeight = ref(window.innerHeight)

/*
  Define functions
*/
const handleResize = () => {
  /**
   * Method to get size of user browser
   */

  windowWidth.value = window.innerWidth
  windowHeight.value = window.innerHeight
};
const onToggleCollapse = () => {
  /**
   * Method to handle collapsed event that trigger by collapsed button in 'sidebar-menu' component.
   */

  // If window width is less or equal 700 (in pixels unit) e.g. for phones, then trigger the toggle method,
  // otherwise do nothing.
  if(Number(windowWidth.value) <= 700){
    storeNavSidebar.value.toggleNavSidebarView();
  }
};

// Life-cycle
onMounted(() => {
    window.addEventListener('resize', handleResize)
});
onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
});

// Watch window width
watch(() => windowWidth.value, (currentValue, oldValue) =>
    {
      // If window width is bigger than 700 (in pixels unit) then show the collapsed nav sidebar,
      // otherwise hide it (e.g. for phones).
      if(Number(currentValue) > 700){
       storeNavSidebar.value.$patch({show: true, collapsed: true});
      }
      else {
        storeNavSidebar.value.$patch({show: false, collapsed: true});
      }
    },
    {
      immediate: true
    }
);

</script>

<style scoped>

</style>