<template>

  <div class="mt-2">
    <multi-select v-model="selectedOption"
                  :options="props.availableSelectByOptions"
                  track-by="value"
                  label="option"
                  :searchable="false"
                  :close-on-select="false"
                  :show-labels="false"
                  :max-height="150"
                  placeholder="Select by"
    />
  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import { MutationType } from 'pinia';
import {useRouter, useRoute} from "vue-router";
import {ref, toRef, defineProps, watch} from 'vue';

export default {
  name: "FilterMultiSelectComponent"
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
  availableSelectByOptions: {
    type: Array,
    required: true
  },
  selectByOption: {
    type: [Object, undefined],
    required: false,
    default: null
  }
});
const storeFilter = toRef(props, 'storeFilter');
const selectedOption = ref(props.selectByOption);
const route = useRoute();
const router = useRouter();

/*
  Keep watching the state of 'storeFilter' and other stores so whenever there is change in
  the state made by another component will make sure to be reflected over the component or the
  view that use that store.

  Note: You can track a certain state property or all properties.

  Info: 1- it will track the change in state of the store only if it's happened using 'direct', 'patch' object
           or $patch function to change the state.
        2- subscribe working in two ways, means if this component cause or tigger anything that will
           lead to change the state of store by other components (like in parent component), will trigger
           mutation type ('direct', 'patchObject' or 'patchFunction') depending on how you are changing the
           state in parent component, then this component will receive that mutation type.

  Important: be careful, the mutation cause by this component should not use as condition to update
             your data, because this will lead to loop.
 */
storeFilter.value.$subscribe((mutation, state) => {
  // You can specify type of mutation.
  if ( [MutationType.patchObject].includes(mutation.type) ) {

    selectedOption.value = state.selectByOption;

  }

  // You can persist the whole state to the local storage whenever it changes.
  // localStorage.setItem('checkedOptions', JSON.stringify(state));

});

// Watch the selectValue object.
watch(() => selectedOption.value, (currentValue, oldValue) =>{

  if (currentValue !== null) {
    router.push({
      name: route.name,
      query: {...route.query, selectBy: currentValue['value'], page: 1}
    });
  }
  else {
    delete route.query.selectBy;
    router.push({path: route.path, query: {...route.query, page: 1}});
  }
});

</script>

<style >

/* multi select style will not work if it set inside <style scoped>  */

.multiselect{
  cursor: default;
  width: 160px;
  font-size: 12px;
  color: #464646;
  transition: all 200ms ease;
  min-height: 43px;
}

.multiselect__single{
  font-size: 12px;
  font-weight: 700;
}

.multiselect__option--highlight{
  background: #e9ecef;
  color: #0F1111;
  transition: color 200ms ease-in-out;
}

.multiselect__tag,
.multiselect__tag-icon::after,
.multiselect__option--selected,
.multiselect__option--selected.multiselect__option--highlight{
  background: #0F1111;
  color: #fff;
  transition: color 200ms ease-in-out;
}

.multiselect__option--selected,
.multiselect__option--selected.multiselect__option--highlight{
  border: 1px solid #e9ecef;
}

.multiselect__tag-icon:hover{
  transition: 0.3s;
  transform: scale(110%);
}

</style>