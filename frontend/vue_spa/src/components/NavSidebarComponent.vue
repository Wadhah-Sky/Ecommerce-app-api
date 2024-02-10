<template>

  <sidebar-menu ref="sidebar"
                :menu="storeNavSidebar.menu"
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
import { useSwipe } from '@vueuse/core';

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
const windowWidth = ref(window.innerWidth);
// To get device height use, ref(screen.height)
const windowHeight = ref(window.innerHeight);
const sidebar = ref();
const { lengthX } = useSwipe(
    sidebar,
    {
      /*
        By marking a touch or wheel listener as passive, the developer is promising the handler won't
        call preventDefault() to disable scrolling. This frees the browser up to respond to scrolling immediately
        without waiting for JavaScript, thus ensuring a reliably smooth scrolling experience for the user.
       */
      // Note: since this swipe is related to plugin component that use events, so using passing as false
      //       will stop these events.
      passive: true,
      // onSwipeEnd is similar to touch event ontouchend (A finger is removed from a touch screen).
      onSwipeEnd(e) {

        // Check that length for X-Axis is less than zero (moving to the right side the moment touch detect
        // on sidepanel) and its value should be more than 50 Pixels
        if(lengthX.value > 0 && lengthX.value > 50){

          // If window width is bigger than 700 (in pixels unit) then show the collapsed nav sidebar,
          // otherwise hide it (e.g. for phones).
          if (Number(windowWidth.value) > 700) {
            storeNavSidebar.value.$patch({show: true, collapsed: true});
          }
          else {
            storeNavSidebar.value.$patch({show: false, collapsed: true});
          }
        }
      },
    },
);

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
    window.addEventListener('resize', handleResize, {passive: false});
});
onUnmounted(() => {
    window.removeEventListener('resize', handleResize, {passive: false});
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