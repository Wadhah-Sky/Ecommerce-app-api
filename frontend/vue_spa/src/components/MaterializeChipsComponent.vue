<template>

    <div class="scroll-menu mt-2">

      <template v-if="selectByObj">

        <div class="chip">
          {{ selectByObj['option'] }}
          <span class="closebtn" @click="removeSelectByOption">&times;</span>
        </div>

      </template>

      <template v-for="(option, index) in options" :key="index">

        <div v-show="option" class="chip">
          {{ option }}
          <span class="closebtn" @click="removeAttrOption(index)">&times;</span>
        </div>

      </template>

      <template v-for="(key, index) in Object.keys(priceObj)" :key="index">

        <div v-if="priceObj[key]" class="chip">
          {{ key === 'minPrice' ? 'min price' : 'max price'}} ${{priceObj[key]}}
          <span class="closebtn" @click="removePrice(key)">&times;</span>
        </div>

      </template>

    </div>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {toRef, ref, defineProps} from "vue";

export default {
  name: "MaterializeChipsComponent"
}
</script>

<script setup>

/*
   Note: this component don't need $subscribe method for 'storeFilter' to watch
         changes of state, that's because whenever 'StoreMainComponent' is rendered will pass
         the new state of the store to this component.
 */

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storeFilter: {
    type: Object,
    required: true
  }
});
const storeFilter = toRef(props, 'storeFilter');
const selectByObj = ref(storeFilter.value.selectByOption)
const options = ref(storeFilter.value.checkedOptions);
const priceObj = ref(storeFilter.value.price);

// Define methods
const removeSelectByOption = () => {
  /**
   * Method to re-set selectByOption, and trigger mutation type of patch object.
   */

  // Re-set price value using key.
  selectByObj.value = null;
  /*
    Change state of 'selectByOption' in filter store.
    Note: Here we prefer to use patch object because this type being watched in 'MultiSelectComponent' by
          subscribe method.
   */
  storeFilter.value.$patch({
    selectByOption: null
  });

};
const removeAttrOption = (index) => {
  /***
   * Method to remove item from 'options' using index, and trigger mutation type of patch object.
   */

  /*
   Remove item from options using index.

   Note: since options is directly connected to store filter 'checkedOptions', so when you make
         a change on 'options' will lead to change 'checkedOptions' in store and this will trigger
         mutation type 'direct'.
         Here we prefer to use patch object because this type being watched in 'FilterAttributeComponent'
         by subscribe method.
   */
  options.value.splice(index, 1);

  storeFilter.value.$patch({
    checkedOptions: options.value
  });

  /* Here we don't need to push our change, because in 'FilterAttributeComponent' we watch()
     any change happen to 'checkedOptions' and push() it, while updating the variable that
     connected to 'checkedOptions' using $subscribe.
   */
  // Push 'options' as string seperated by comma (,).
  // router.push(
  //     {
  //       path: route.path,
  //       query: {...route.query, attr: options.join(), page: 1}
  //     }
  // );
};
const removePrice = (key) => {
  /**
   * Method to re-set price of 'priceObj' using key, and trigger mutation type of patch object.
   */

  // Re-set price value using key.
  priceObj.value[key] = null;
  /*
    Change state of 'price' using key in filter store.
    Note: Here we prefer to use patch object because this type being watched in
          'PriceRangeComponent' by subscribe method.
   */
  storeFilter.value.$patch({
    price: {key: null}
  });

};

</script>

<style scoped>

div.scroll-menu {
  overflow: auto;
  white-space: nowrap;
}

div.scroll-menu::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
}

div.scroll-menu{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

div.scroll-menu .chip {
  display: inline-block;
  margin-right: 11px;
}

.chip {
  color: #464646;
  display: inline-block;
  padding: 3px 6px 3px 7px;
  font-size: 12px;
  border-radius: 25px;
  background-color: #e9ecef;
}

.chip:hover,
.chip:hover .closebtn{
  color: #fff;
  background-color: #0F1111;
  transition: scale 0.2s;
}

.closebtn {
  padding-left: 10px;
  color: #464646;
  font-weight: bold;
  float: right;
  font-size: 12px;
  cursor: pointer;
}

.closebtn:hover {
  color: #0F1111;
}

</style>