<template>

  <template v-if="Object.keys(productOptions).length > 0">

    <div style="display: inline-block">
      <div v-if="storeProduct.dataLoading">
        <font-awesome-icon :icon="['fa-solid', 'spinner']"
                           style="color: #0f1111; font-size: 15px;"
                           spin
        />
        Loading
      </div>
    </div>

    <div v-for="(options, index) in productOptions" :key="index" class="row">

      <template v-if="options.length > 1">

        <div class="item-option-select mt-2">

          <template v-if="(useColorShape && colorSyllable.includes(lowerCase(index))) ||
                          (useImg && risePickerSyllable.includes(lowerCase(index))) &&
                          !selectedSameOptionStatus[index]"
          >

            <div class="row">

              <div class="col">

                <label class="typo__label">
                  {{index?.charAt(0).toUpperCase() + index?.slice(1)}}
                </label>
                <span style="font-weight: 600;">{{selectLabel[index]}}</span>

              </div>

            </div>

            <product-single-select-component v-model="selectedOption[index]"
                                             :group-name="index"
                                             :options="options"
                                             :use-img="useImg ? checkThumbnailsAvailability(index) : false"
                                             track-by="value"
                                             parent-attr="parentAttribute"
                                             @mouseenter="setSelectLabel(index, $event.label)"
                                             @mouseleave="setSelectLabel(index, $event.label)"
                                             @change="Object.keys(productOptions).length > 1 ?
                                              updateProductOptionsStatus(
                                                  index,
                                                  $event.option,
                                                  false,
                                                  !($event.target.checked)
                                              ) : ''"

            />

          </template>

          <template v-else>

            <div class="row justify-content-between" style="width: 200px">

              <div class="col-10">

                <label class="typo__label">{{ index?.charAt(0).toUpperCase() + index?.slice(1) }}</label>

              </div>

              <div v-if="Object.keys(productOptions).length > 1"
                   class="col-1"
                   @click="resetOption(index)"
                   v-tooltip
                   data-bs-toggle="tooltip"
                   data-bs-placement="top"
                   :title="`deselect ${lowerCase(index)}`"
              >

                <font-awesome-icon icon="fa-solid fa-xmark"/>

              </div>

            </div>

            <multi-select v-model="selectedOption[index]"
                          :options="options"
                          :multiple="selectedSameOptionStatus[index]"
                          :preselect-first="true"
                          track-by="value"
                          label="value"
                          :searchable="false"
                          :close-on-select="!selectedSameOptionStatus[index]"
                          :show-labels="false"
                          :allow-empty="Object.keys(productOptions).length > 1"
                          :max-height="150"
                          @select="Object.keys(productOptions).length > 1 ?
                            updateProductOptionsStatus(index, $event, selectedSameOptionStatus[index]) : ''"
                          @remove="Object.keys(productOptions).length > 1 ?
                            updateProductOptionsStatus(index, $event, selectedSameOptionStatus[index], true) : ''"
                          :placeholder="selectedSameOptionStatus[index] ? 'Pick multiple values' : 'Pick a value'"
                          :disabled="storeProduct.dataLoading"
            />
          </template>
        </div>

        <!--        <div class="item-option-select">-->

        <!--          <h6>Choose Color</h6>-->

        <!--          <div class="btn-group btn-group-sm btn-group-toggle"-->
        <!--               data-toggle="buttons"-->
        <!--          >-->

        <!--            <label class="btn btn-light">-->
        <!--              <input type="radio" name="radio_color"> Silver-->
        <!--            </label>-->

        <!--          </div>-->
        <!--        </div>-->

      </template>

    </div> <!-- row.// -->

    <hr>

  </template>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import ProductSingleSelectComponent from "@/components/ProductSingleSelectComponent";
import {useRouter, useRoute} from "vue-router";
import{ref, toRef, defineProps, defineEmits, watch, onMounted} from "vue";

export default {
  name: "ProductSelectComponent",
  components: {
    ProductSingleSelectComponent
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storeProduct: {
    type: Object,
    required: true
  },
  triggerGetDataResult:{
    type: Function,
    required: true
  }
});
const storeProduct = toRef(props, 'storeProduct');
const productOptions = ref(storeProduct.value.productOptions);
// selected option should looks like below:
// {'Color': [{'value': 'Black'}, {'value': 'Ocean blue'}], 'Size': [{'value': '38'}]}
const selectedOption = ref(storeProduct.value.selectedProductItemOptions);
const selectedSameOptionStatus = ref(storeProduct.value.selectedProductItemSameOptionsStatus);
const productOptionsCombination = ref(storeProduct.value.productOptionsCombination);
const productItemsSlugs = ref(storeProduct.value.productItemsSlugs);
const useColorShape = storeProduct.value.dataResult['use_item_attribute_color_shape'];
const useImg = storeProduct.value.dataResult['use_item_attribute_img'];
const router = useRouter();
const route = useRoute();
const selectLabel = ref({});
const risePickerSyllable = ['rise', 'picker', 'rise style', 'rise picker', 'rise picker style'];
const colorSyllable = ['color', 'colors', 'colour', 'colours'];
// Define the list of events that you want to emit.
const emits = defineEmits(['activeOption']);

/*
 elements variable, is a ref to html elements.
 in loop can do to set dynamic reference:
 <element-tag :ref="(el) => (elements[index] = el)" </element-tag>
 */
// const elements = ref({});

/*
  Define functions
*/
const checkThumbnailsAvailability = (index) => {
  /**
   * Method to check array of options that should all of them has thumbnail value, otherwise return false.
   */

  // Get the option array.
  let arr = productOptions.value[index];
  // return true if condition is passed for all objects of array otherwise return false.
  return !!arr.every(item => !['', null, 'None', false].includes(item.thumbnail));
};
const setSelectLabel = (index, label) =>{
  /**
   * Set value for specific index in 'selectLabel' variable reference.
   */
  selectLabel.value[index] = label;
}
const lowerCase = (value) => {
  /**
   * Method to lower case any provided string.
   */
  // Note: you need to check if value is not none, otherwise will raise an exception undefined value.
  return value?.toLowerCase();
};
const resetOption = (index) => {
  /**
   * Method to reset multi-select selected options to be null.
   */

  /*
    Note: the value of selectedOption.value[index] can be:
          1- array of objects/object whether it's come from multi-select with multiple is true or not.
          2- single object whether it's come from multi-select with multiple is true or not.
   */
  // Store the array/object of selectedOption.value[index]
  let selected = selectedOption.value[index];

  // Check that 'selected' is not null.
  if (selected !== null) {

    // Check if current 'selected' is a multiple multi-select and has multiple objects selected,
    // so tigger the 'updateProductOptionsStatus' method for whole selected option objects.
    if (selectedSameOptionStatus.value[index] && Object.values(selected).length > 1) {
      updateProductOptionsStatus(index, selected, true, true);
    }
    else if (Array.isArray(selected)){
      // In case the current 'selected' is an array of objects/object. so trigger the 'updateProductOptionsStatus'
      // method for each object.
      for (let obj of selected) {
        updateProductOptionsStatus(index, obj, false, true);
      }
    }
    else {
      // In case current 'selected' is only a single object, so tigger the 'updateProductOptionsStatus' method for it.
      updateProductOptionsStatus(index, selected, false, true);
    }

  // Reset the selectedOption.value[index] to be null.
  selectedOption.value[index] = null;
  }
};
const duplicates = async (arr) => {
  /**
   * Return an array (non duplicates values) of duplicated values in the given array.
   */

  /*
    Info: about filter() method:
          1- Creates a new array filled with elements that pass a test provided by a function.
          2- Does not execute the function for empty elements, and return empty array in this case.
          3- Does not change the original array.

          Syntax: array.filter(function(currentValue, index, arr), thisValue)

                  1- function():	Required. A function to run for each array element.
                  2- currentValue:	Required. The value of the current element.
                  3- index:	Optional. The index of the current element.
                  4- arr:	Optional. The array of the current element.
                  5- thisValue:	Optional. Default undefined, A value passed to the function as its this value.

          Return Value: array, containing the elements that pass the test. If no elements pass the test
                        it returns an empty array.
   */

  // after got the array of duplicated values, make new array of set for returned array.
  return [...new Set(arr.filter((e, i, a) => a.indexOf(e) !== i))]
}
const updateProductOptionsStatus = async (index, selectedObj, multi=false, removed=false) => {
  /**
   * Method that triggered when select/de-select product option.
   *
   * Note: this method is supposed to handle object of single multi-select and array of objects
   *       of multiple multi-select.
   */

  // Initialize an object to store objects and its values.
  let dictionary = {};

  // Check if trigger come from product option related to multi-select with attribute :multiple is true.
  // if so, check that related selectedOption contains more than one element.
  if (multi === true && Object.values(selectedOption.value[index]).length > 1) {

    /*
       The idea of this part of the code is to get combination for each selected product option object
       of multiple multi-select, after that loop over the product options and get duplicated values between them
       in the combination, the duplicated values array will be the dictionary of continuing process.
     */

    // Initialize an empty object to store key: option of selected options, while value: its combination object.
    let dictOfObj = {};
    // Initialize an empty object to store duplicated value of chosen selected options.
    let commonDict = {};

    // Loop over value (array) of objects.
    for (let obj of selectedOption.value[index]) {
      // in Javascript, object parameter passed by value by its keys passed by reference, so it's better
      // to clone the obj that you will change its keys.
      dictOfObj[obj.value] = structuredClone(productOptionsCombination.value[index][obj.value]);
    }

    // Loop over keys of dictOfObj.
    for (let key in dictOfObj) {

      // Get array of [index, val] of dictOfObj[key], where 'index' is key name, while 'value' they key array of values.
      for (let [index, val] of Object.entries(dictOfObj[key])) {

        // Check that 'commonDict' if already has key name (index) as property or not.
        /*
           Here we are using hasOwnProperty() method as alternative to below code:

           if(!commonDict[index]){}

           Of course, the code below assumes that:

           1- The global Object has not been shadowed or redefined.
           2- The native Object.prototype.hasOwnProperty() has not been redefined.
           3- No 'call' own property has been added to Object.prototype.hasOwnProperty()
           4- The native Function.prototype.call() has not been redefined.

         */
        if (!Object.prototype.hasOwnProperty.call(commonDict, index)) {
          // Set key and its value (array of values) into commonDict.
          commonDict[index] = val;
        }
        else {
          // If exists the index as key in commonDict, then updated its value (array) with new values.
          for (let item of Object.values(val)) {
            commonDict[index].push(item);
          }
        }

        // find duplicates and store it in dictionary object where index it's the key and duplicated array as value.
        dictionary[index] = await duplicates(commonDict[index]);
      }
    }
  }
  else {
    // In this case, a single object has passed of multiple/single multi-select, so get its combination.
    dictionary = structuredClone(productOptionsCombination.value[index][selectedObj.value]);
  }

  // Loop over each key of dictionary.
  for (let key of Object.keys(dictionary)) {

    // Check that the current key is found in elements variable.
    /*
      Note: Maybe in case you got a product option of single value so no need to show
            multi-select to the user of that option and no need add that option into element array.
    */
    // if (elements.value[key]) {

    if(Object.values(productOptions.value[key]).length > 1) {

      // Loop over elements options for certain key.
      // for (let optionObj of elements.value[key].options) {

      for (let optionObj of productOptions.value[key]) {

        // In case this method triggered with 'removed' is false. Then which element[key] option value
        // if found in the dictionary for same key, set '$isDisabled' to be true if it's not found and
        // false if it's found.
        // Here if you are trying to change value of product store variable state, no need to do $patch.
        if (removed === false) {
          optionObj.$isDisabled = !Object.values(dictionary[key]).includes(optionObj.value);
        }
        else if (!Object.values(dictionary[key]).includes(optionObj.value)) {
          // In case 'removed' is true and option value if found in the dictionary for same key, then set
          // '$isDisabled' for that option as false.
          optionObj.$isDisabled = false;
        }
      }
    }
  }
};

// Life-cycle, Note that OnMounted can be triggered if component code is updated.
onMounted( () => {

  /*
    Note: the value of selectedOption.value[index] will be, array of objects/object whether it's come
          from multi-select with multiple is true or not.
   */

  // No need to trigger 'updateProductOptionsStatus' method if elements variable has no more than one object
  // and 'productOptions' has no more than one object.

  // if (Object.keys(productOptions.value).length > 1 && Object.keys(elements.value).length > 1) {

  // productOption => {color: [{}, {}], size: [{}]}
  if (Object.keys(productOptions.value).length > 1 ){

    // Loop over selected options.
    // selectedOption => {color: [{}, {}], size: [{}]}
    // key => color, size ..etc
    for (let key of Object.keys(selectedOption.value)) {

      // Check if 'productOptions' for current selected option key has array of more than one item.
      if (Object.values(productOptions.value[key]).length > 1) {

        // Check if current selected option key is a multiple selected values AND this key in selectedOption
        // is already has array of more than one object. so tigger the 'updateProductOptionsStatus' method
        // for whole selected option objects.
        if (selectedSameOptionStatus.value[key] && Object.values(selectedOption.value[key]).length > 1) {

          updateProductOptionsStatus(key, selectedOption.value[key], true);
        }
        else if (Array.isArray(selectedOption.value[key])) {
          // Since value of the current key for selectedOption is an array (have one element), loop over it.
          for (let obj of selectedOption.value[key]) {
            updateProductOptionsStatus(key, obj);
          }
        }
        else {
          // In case happen to be selectedOption.value[key] is an object and not an array.
          updateProductOptionsStatus(key, selectedOption.value[key]);
        }
      }
    }
  }

  // Emit a signal to parent component.
  emits('activeOption', {status: true});

});

// Watch effects, access ref elements after our component is rendered.
// watchEffect(() =>
//     {
//       setOptionsCombinations();
//     },
//     {
//       // Make watch effect run after the component is updated.
//       flush: "post"
//     }
// );


// Watch the selectOption object.
watch(() => selectedOption.value, (currentValue, oldValue) =>
    {

      /*
       Notice: current value for v-model object in case
               1- there multiple values to pick for each multi-select is an array/empty array.
               2- only single value to pick for each multi-select is an array/null.
               3- only one multi-select is available with single value to pick is an object/null (But we
                  set in this specific case to always to pick value with no possible of unselect using
                  attribute of :allow-empty to be false).
       */

      // Initialize an empty array variable.
      let attributes = [];
      // Initialize an empty variable to hole the wanted product item slug.
      let product_item_slug = null;
      // Set boolean variable that we use if it's true will allow to make router push.
      let pushStatus = false;

      // Loop over currentValue object which represent selected options, where 'index' represent key
      // while 'val' represent its value (array of objects).
      for (let [index, val] of Object.entries(currentValue)) {

        // In case current key for currentValue is an array and not empty
        if (Array.isArray(currentValue[index]) && currentValue[index].length > 0) {

          // Loop over 'val' array of objects.
          for (let item of val) {

            attributes.push(item.value);
          }
        }
        // In case current key for currentValue is not null object.
        else if(currentValue[index] !== null) {
          attributes.push(currentValue[index].value);
        }
      }

      // Check if attributes array is not empty.
      if (attributes.length > 0) {

        // Loop over value (array) of 'productItemsSlugs'.
        // productItemsSlugs => [{<item_slug>: [<related_attributes>]}, {<item_slug>: [<related_attributes>]}]
        for (let [index, val] of Object.entries(productItemsSlugs.value)) {

          // Make sure:
          // 1- the current val (array) length is equal to attributes array.
          // 2- and the whole array items included within array of attributes.
          if (val.length === attributes.length && val.every(item => attributes.includes(item))) {
            // set the value of 'product_item_slug'
            product_item_slug = index;
            // Set push status to be true.
            pushStatus = true
            // No need to continue loop over the rest arrays.
            break;
          }
        }

        /////////////////////////////////////////////////////////////////
        // In case want to use 'itemS' query parameter.
        ////////////////////////////////////////////////////////////////
        // In case push status is true and product item slug is not null, push new router state.
        if (pushStatus && product_item_slug !== null) {

          // Check that the current route.query.itemS is not equal to selected product item slug.
          if(route.query.itemS !== product_item_slug){

            // Tigger the passed function through props with required parameters, to get data from backend server.
            // 'getProductItemDataResult' method parameters : (method, slug, itemS, attr=null, onlyItem=false)
            props.triggerGetDataResult(
                'getProductItemDataResult',
                route.params.slug,
                product_item_slug,
                null,
                true
            );

            // If everything went ok to restore data from backend server, push new router state.
            router.replace({
              name: route.name,
              query: {'itemS': product_item_slug}
            });
          }

          // Emit a signal to parent component.
          emits('activeOption', {status: true});
        }
        else {
          // Emit a signal to parent component.
          emits('activeOption', {status: false});
        }

        /////////////////////////////////////////////////////////////////
        // In case want to use 'attr' query parameter.
        ////////////////////////////////////////////////////////////////
        // In case push status is true, push new router state.
        // if (pushStatus) {
        //
        //   let currentRouteAttr = route.query.attr.trim().split(',');
        //
        //   if (!(currentRouteAttr.length === attributes.length && currentRouteAttr.every(item => attributes.includes(item)))) {
        //
        //     // Convert attributes array to string seperated by comma.
        //     let attributesString = attributes.join();
        //
        //     // Tigger the passed function through props with required parameters, to get data from backend server.
        //     // 'getProductItemDataResult' method parameters : (method, slug, itemS, attr=null, onlyItem=false)
        //     props.triggerGetDataResult(
        //         'getProductItemDataResult',
        //         route.params.slug,
        //         route.query.itemS,
        //         attributesString
        //         true
        //     );
        //
        //     // If everything went ok to restore data from backend server, push new router state.
        //     router.replace({
        //       name: route.name,
        //       query: {'attr': attributesString}
        //     });
        //
        //     // Emit a signal to parent component.
        //     emits('activeOption', {status: true});
        //   }
        // }
        // else{
        //   Emit a signal to parent component.
        //   emits('activeOption', {status: false});
        // }
      }
    },
    {
      deep: true
    }
);

</script>

<style scoped lang="scss">

.fa-xmark{
  cursor: pointer;
  display: inline-block;
  font-size: 18px;
  color: #0f1111;
}

.fa-xmark:hover{
  color: rgb(204, 12, 57);
  transition: 0.3s;
}

</style>

<style>

/* multi select style will not work if it set inside <style scoped>  */

.multiselect{
  margin: 0;
  padding: 0;
  cursor: default;
  min-width: 206px;
  max-width: 206px;
  font-size: 13px;
  color: #464646;
  transition: all 200ms ease;
  min-height: 45px;
}

.multiselect__single{
  font-size: 13px;
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

.multiselect__option--disabled{
}

.multiselect__tag-icon:hover{
  transition: 0.3s;
  transform: scale(110%);
}

.typo__label::after{
  content: ':';
  padding-right: 4px;
}
</style>