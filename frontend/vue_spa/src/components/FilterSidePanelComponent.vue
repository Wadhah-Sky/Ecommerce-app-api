<template>

  <div ref="sidePanel" class="sidepanel">
    <span ref="span" class="header">
      Filters
    </span>
    <div class="line"></div>
    <div ref="circle" class="circle" @click="triggerToggleSidePanel">
      <i :class=" isHide ? 'hide' : '' " aria-hidden="true">
        <font-awesome-icon :icon="['fa-solid', 'fa-chevron-left']"/>
      </i>
      <i :class=" !isHide ? 'hide' : '' " aria-hidden="true">
        <font-awesome-icon :icon="['fa-solid', 'fa-chevron-right']"/>
      </i>
    </div>

    <div class="container mt-4">

      <div class="row ">

        <div class="col-md-4 offset-9">
          <router-link :to="{ name: route.name, query: {page: 1} }"
                       v-slot="{ href, isActive, isExactActive }"
                       custom
          >
            <a class="reset-link"
               :href="href"
               :class="[isActive ? 'router-link-active' : '', isExactActive ? 'router-link-exact-active' : '']"
               @click.prevent="resetFilters"
               :style="[ href === route.fullPath ? {pointerEvents: 'none', display: 'inline-block', backgroundColor: '#e9ecef', color: '#464646'} : '']"
            >
              Reset
            </a>
          </router-link>
        </div>

      </div>

    </div>


    <div class="container" style="margin: 0; padding: 0">

      <div v-if="!storeFilter.dataLoading" class="row scroll-menu">

        <div class="row">

          <multi-select-component :store-filter="storeFilter" />

        </div>

        <div class="row mt-4">

          <span class="attribute">Avg. Customer Review</span>

          <rating-stars-component/>

        </div>

        <div class="row mt-1">

          <span class="attribute">Price</span>

          <price-range-component :store-filter="props.storeFilter"/>

        </div>

        <filter-attribute-component :data="storeFilter.dataResult"
                                    :store-filter="props.storeFilter"
        />

      </div>

      <div v-else>
        <content-loader-component style="transition: all 0.3s ease-in-out"/>
      </div>

    </div>

  </div>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import FilterAttributeComponent from "@/components/FilterAttributeComponent";
import MultiSelectComponent from "@/components/MultiSelectComponent";
import RatingStarsComponent from "@/components/RatingStarsComponent";
import PriceRangeComponent from "@/components/PriceRangeComponent";
import {useRoute, useRouter} from "vue-router";
import {ref, toRef, onMounted, defineExpose, defineProps} from "vue";

export default {
  name: "FilterSidePanelComponent",
  components: {
    ContentLoaderComponent,
    FilterAttributeComponent,
    MultiSelectComponent,
    RatingStarsComponent,
    PriceRangeComponent
  }
}

</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storeFilter: {
    type: Object,
    required: true
  },
  endpoint: {
    type: String,
    required: true
  },
  slug: {
    type: String,
    required: true
  }
});
const storeFilter = toRef(props, 'storeFilter');
const route = useRoute();
const router = useRouter();
const sidePanel = ref();
const span = ref();
const circle = ref();
const currentSidePanelWidth = ref();
const isHide = ref(false);

/*
  Define functions
*/
const triggerGetDataResult = async (endpoint) => {
  /**
   * Function to trigger store method to get data from backend.
   */

  // Trigger the method to get the data result from backend in case store 'response' object
  // value is empty (have no keys).
  if (!( Object.keys(storeFilter.value.response).length )) {
    // Tigger the method to get data from backend.
    await storeFilter.value.getDataResult(endpoint);
  }
}

const triggerToggleSidePanel = () => {
  /**
   * Function to open and close the filter side panel.
   */

  // Change the state of 'collapsed' in the filter store.
  // Note: if collapsed value is false means the sidepanel is closing/closed.
  storeFilter.value.toggleCollapsedState();

  // Call for triggerGetDataResult method.
  triggerGetDataResult(props.endpoint + `${props.slug}/`);

  /* select the html element from the DOM. */
  // const sp = document.querySelector(".sidepanel");
  /*
    If you want to get a value of style property of specific html element:
    1- directly using its 'ref' or after selecting it using 'document.querySelector/getElementByID', for example:
       A- <ref>.value.style.<property>
       B- <selectedElement>.style.<property>
    2- if the style property is computed (means it's not defined within the element tag, it's defined within
       <style> tag or in separate css file), in this case you can get the value for that property using
       'getComputedStyle(<selectedElement>)', remember it's read only value, if you want to change it?
       A- You can do it by using:
          <selectedElement>.style.setProperty('<property>', 'newValue')
       B- using 'ref' like:
          <ref>.value.style.<property> = newValue

       Note: set a value for property will not change its value in css file, only for the current mounted DOM.
  */
  // Get width value for specific element from computed style.
  // const { width: currentWidth} = getComputedStyle(sp);

  // Get current width value of side panel div from 'currentSidePanelWidth' object.
  let w = currentSidePanelWidth.value;

  // Note: when you set a ref to html element, you can access to any of its directive attributes directly.
  /*
    Note: no matter if the value of specific style property is stored as % or decimal it's always return
          as string of (decimal+px).
  */
  // radix for parseInt() function it's the base for converting value.
  const currentMarginRight = parseInt(sidePanel.value.style.marginRight, 10);

  /*
    If current margin-right is equal or bigger than zer (means the side panel is open) then set the value
    for margin-right as minus width of div of side panel, otherwise set it to 0 (change it from negative to
    positive) which means the side panel is close, so we want to open it.
  */
  const newMarginRight = ( currentMarginRight >= 0 ) ? ( w * -1 ) : 0;
  /*
    The same thing with right value for div of circle, but we use value of newMarginRight in positive
    (minus*minus) to position circle in the far right in case the side panel is close while if it's open
    we use its width's value minus 22px.
  */
  const newCircleRight = ( newMarginRight < 0 ) ? -newMarginRight : ( w - 22 );

  // Set the new value for style properties.
  sidePanel.value.style.marginRight = span.value.style.marginRight = `${newMarginRight}px`;
  circle.value.style.right = `${newCircleRight}px`;

  // Toggle 'isHide' value.
  isHide.value = !isHide.value;
};
const resetFilters = async () => {
  /**
   * Method to push new router state and update/re-render side panel component.
   */

  // Push new router state.
  router.push({name: route.name, query: {page: 1}});

  // Reset the 'response' of storeFilter using patch function.
  props.storeFilter.$patch((state) => {
    state.response = {};
  });

  // Now you can trigger 'triggerGetDataResult' method, which will force re-render side panel component,
  // which means update self/children data.
  await triggerGetDataResult(props.endpoint + `${props.slug}/`);
};

// const updateArray = (input) =>{
// /**
//    Update array value.
//  */
//
// modelArray.value = [...modelArray.value, input];
//
// };

// When the view is mounted we can reach the 'document' object.
onMounted( () => {

  const sp = document.querySelector(".sidepanel");
  const style = getComputedStyle(sp);
  currentSidePanelWidth.value = parseInt(style.width, 10);

});

// Expose the functions/variables that we want to trigger/use from the parent component.
defineExpose({triggerToggleSidePanel, triggerGetDataResult});

</script>

<style scoped lang="scss">

.attribute {
  line-height: 16px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
}

.sidepanel {
  position: fixed;
  top: 0;
  right: 0;
  height:100vh;
  background-color: #fff;
  width:100%;
  max-width:290px;
  margin-right:-290px;
  color:#0F1111;
  transition: 0.8s ease;
  z-index:99;
}
.sidepanel:after {
  content:'';
  position:absolute;
  height:100vh;
  width:10px;
  top:0;
  right:100%;
  background-image: linear-gradient(to right,#fff,#aaa 15px);
  z-index:1;
}
.sidepanel .header {
  font-size:1.5em;
  line-height:1.5em;
  text-align:center;
  font-weight: bold;
  position:relative;
  display:block;
  width:calc(100% - 2em);
  max-width:290px;
  padding:1em;
  background-color:#fff;
  transition: 1s ease;
}
.line {
  width:calc(100% - 44px);
  /*background-color:#E9D985;*/
  /*margin:0 22px;*/
  background-color: #0F1111;
  height: 1px;
  margin: 0 20px;
}
.circle {
  position:absolute;
  width:44px;
  height:44px;
  border-radius:50%;
  font-size:16px;
  background-color:#0F1111;
  color:#f1f1f2;
  display:flex;
  justify-content:center;
  align-items:center;
  top:calc(12% - 22px);
  right:calc(100% - 0px);
  z-index:3;
  cursor:pointer;
  opacity: 0.6;
  transition: 1s ease, opacity 200ms ease-in-out;

}
.circle:hover {
  opacity: 1;
}
.fa-chevron-right {
  margin-left:5px;
}
.fa-chevron-left {
  margin-right:5px;
}
.hide {
  display:none;
}


.scroll-menu{
  max-height: 78vh;
  overflow-y: auto;
  margin: 0;
  padding: 0;
}

::-webkit-scrollbar {
  width: 6px;
  border-radius: 4px;
  z-index: 99;
  opacity: 0;
  transition: 0.3s opacity ease;
}

/* Track */
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px #fff;
    -webkit-border-radius: 4px;
    border-radius: 4px;
    cursor: pointer;

}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 4px;
  border-radius: 4px;
  background: #aaa;
  -webkit-box-shadow: inset 0 0 6px #fff;
  transform: translate(0%);
  display: block;
  opacity: 1;
  cursor: pointer;
  user-select: none;
  transition: 0.3s opacity ease;
}

.reset-link{
  display: inline-block;
  color: #464646;
  text-decoration: none;
  background-color: #fff;
  padding: 4px 3px;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}
.reset-link:hover{
  transition: color 200ms ease-in-out;
  color: #fff;
  background-color: #0F1111;
}

</style>


<!--<div class="arrow"></div>-->

<!--<style lang="sass">-->

<!--/*Scroll mouse animation*/-->

<!--.arrow,-->
<!--.arrow:before-->
<!--  position: absolute-->
<!--  left: 50%-->

<!--.arrow-->
<!--  width: 25px-->
<!--  height: 25px-->
<!--  top: 94%-->
<!--  margin: -20px 0 0 -20px-->
<!--  -webkit-transform: rotate(45deg)-->
<!--  border-left: none-->
<!--  border-top: none-->
<!--  border-right: 2px #0F1111 solid-->
<!--  border-bottom: 2px #0F1111 solid-->
<!--  overflow-y: auto-->


<!--.arrow:before-->
<!--  content: ''-->
<!--  width: 15px-->
<!--  height: 15px-->
<!--  top: 50%-->
<!--  margin: -10px 0 0 -10px-->
<!--  border-left: none-->
<!--  border-top: none-->
<!--  border-right: 1px #0F1111 solid-->
<!--  border-bottom: 1px #0F1111 solid-->
<!--  animation-duration: 2s-->
<!--  animation-iteration-count: infinite-->
<!--  animation-name: arrow-->

<!--@keyframes arrow-->
<!--  0%-->
<!--    opacity: 1-->
<!--  100%-->
<!--    opacity: 0-->
<!--    transform: translate(-10px, -10px)-->


<!--</style>-->