<template>

  <div class="row-cols-auto mt-1">

    <template v-if="risePickerSyllable.includes(lowerCase(groupName)) || props.useImg">

        <label v-for="( option ) in options"
               :key="whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')"
               :for="whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')"
               :tabindex="option.$isDisabled ? -1 : 0"
               class="option-img-check-label"
               @mouseenter="emits('mouseenter', {label: option[`${trackBy}`]})"
               @mouseleave="setCheckedOptionLabel"
        >
          <input type="radio"
                 ref="inputs"
                 :name="whiteSpacesReplace(lowerCase(groupName), '-')"
                 :disabled="option.$isDisabled"
                 :checked="checkedValues?.includes(option[`${trackBy}`])"
                 :id="whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')"
                 :value="option[`${trackBy}`]"
                 :tabindex="option.$isDisabled ? -1 : 0"
                 @input="emits('update:model-value', option)"
                 @change="changeOption($event, option)"
          />

          <template v-if="risePickerSyllable.includes(lowerCase(groupName))">

            <span :class="['option-img col', whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')]"></span>

          </template>

          <template v-else-if="props.useImg">

            <span class="option-img col" style="width: 72px!important; height: 72px!important;">
              <img v-lazy="option.thumbnail" :alt="option[`${trackBy}`]" >
            </span>

          </template>


        </label>

    </template>

    <template v-else>

      <label v-for="( option ) in options"
             :key="whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')"
             :for="whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')"
             :tabindex="option.$isDisabled ? -1 : 0"
             class="option-color-check-label"
             @mouseenter="emits('mouseenter', {label: option[`${trackBy}`]})"
             @mouseleave="setCheckedOptionLabel"
      >
        <input type="radio"
               ref="inputs"
               :name="whiteSpacesReplace(lowerCase(groupName), '-')"
               :disabled="option.$isDisabled"
               :checked="checkedValues?.includes(option[`${trackBy}`])"
               :id="whiteSpacesReplace(lowerCase(option[`${trackBy}`]), '-')"
               :value="option[`${trackBy}`]"
               :tabindex="option.$isDisabled ? -1 : 0"
               @input="emits('update:model-value', option)"
               @change="changeOption($event, option)"
        />

        <span :class="['option-color', 'col']"
              :style="{backgroundColor: `#${option[`${parentAttr}`]}`}"
        >
          <font-awesome-icon v-if="!option.$isDisabled" icon="fa-solid fa-circle-check"/>
        </span>

      </label>

    </template>

  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import {whiteSpacesReplacer} from "@/common/whiteSpacesReplacer";
import{ref, defineProps, defineEmits, onMounted} from "vue";

export default {
  name: "ProductSingleSelectComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
// Note: 'modelValue' can be an array or a single object.

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  groupName: {
    type: String,
    required: true
  },
  options: {
    type: Array,
    required: true
  },
  trackBy: {
    type: String,
    required: true
  },
  parentAttr: {
    type: String,
    required: true
  },
  useImg: {
    type: Boolean,
    default: false
  }
});
const modelValue = ref(props.modelValue);
const groupName = ref(props.groupName);
const options = ref(props.options);
const trackBy = ref(props.trackBy);
const parentAttr = ref(props.parentAttr);
const checkedValues = ref([]);
const risePickerSyllable = ['rise', 'picker', 'rise style', 'rise picker', 'rise picker style'];
// static reference to hold single/multiple reference of elements.
const inputs = ref(null);
// Define the list of events that you want to emit.
const emits = defineEmits(
    ['update:model-value', 'change', 'mouseenter', 'mouseleave']
);

/*
  Define functions
*/
const selectedOptions = (selected, updated=false) =>{
  /**
   * Add the 'trackBy' value of provided object/array(objects) into 'checkedValues' array.
   */

  // Initialize an empty list to store checked options value.
  let checkedArray = [];

  if (!updated) {
    // Check the type of object 'selected' is it array or single object.
    if (Array.isArray(selected) && selected.length > 0) {
      for (let obj of selected) {
        checkedArray.push(obj[`${trackBy.value}`]);
      }
    } else {
      checkedArray.push(selected[`${trackBy.value}`]);
    }
  }
  else {
    // Loop over elements (input) those are checked.
    for (let el of inputs.value) {
      if (el.checked) {
        // Get the value attribute of the element.
        checkedArray.push(el.value);
      }
    }
  }

  // Update the 'checkedValues' with new value.
  checkedValues.value = checkedArray;
};
const setCheckedOptionLabel = () => {
  /**
   * Emit the value of checked options when event 'mouseout' is triggered.
   */

  /*
    Info: 'mouseleave' is fired when the pointer has exited the element and all of its descendants,
          whereas 'mouseout' is fired when the pointer leaves the element or leaves one of the element's
          descendants (even if the pointer is still within the element).
   */
  emits('mouseleave', {label: checkedValues.value.join()});
};
const changeOption = (event, option) => {
  /**
   * Emit the 'change' event to parent element and update the 'checkedValues' array with new value.
   */

  // Emit the 'change' event to parent element.
  emits('change', {target: event.target, option: option});

  // Trigger 'selectedOptions' with 'updated' is true.
  selectedOptions(modelValue.value, true);

};
const lowerCase = (value) => {
  /**
   * Method to lower case any provided string.
   */
  // Note: you need to check if value is not none, otherwise will raise an exception undefined value.
  return value?.toLowerCase();
};
const whiteSpacesReplace = (str, use='') => {
  /**
   * Replace all whitespace in the string you need by use global mode (search
   * through whole string).
   */
  return whiteSpacesReplacer(str, use)
};

// Life-cycle
onMounted(() => {
  // Set value/values of modelValue into checkedValues
  selectedOptions(modelValue.value);
  // tigger the event of mouseleave to set the checked option/option label.
  setCheckedOptionLabel();
});

</script>

<style scoped lang="scss">

$option-rise-pickers-background-img: url("../assets/images/swatches/rise-pickers.png");

.option-color {
  background-size: 1700px 500px;
  margin: 0 10px 5px 0.1px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
  cursor: pointer;
}

.option-color:hover{
  transform: scale(120%);
  transition: transform 0.2s;
}

.option-color-check-label {
  position: relative;
}
.option-color-check-label input {
  position: absolute;
  z-index: -1;
  opacity: 0;
}
.option-color-check-label input:disabled ~ .option-color {
  cursor: not-allowed;
  //pointer-events: none;
  opacity: 50%;
  color: transparent !important;
}

.fa-circle-check{
  background-color: #0F1111;
  color: #fff;
  float: left;
  padding: 0;
  margin: 6px 0 0 6px ;
  font-size: 14px;
  font-style: normal;
  font-variant: normal;
  text-rendering: auto;
  -webkit-font-smoothing: antialiased;
  border-radius: 50%;
  opacity: -1;
}

.option-color-check-label input:checked ~ .option-color .fa-circle-check{
  opacity: 1;
}

.option-img{
  height: 49px;
  width: 44px;
  margin: 5px 6px 0 0;
  display: inline-block;
  cursor: pointer;
}

// if you dont use 'max' with height and width, the image will show as resized (fill).
// use transform 'scale' to show image in good shape.
.option-img img{
  vertical-align: top;
  overflow-clip-margin: inherit;
  overflow: clip;
  //transform: scale(0.8);
  margin: 2px;
  padding: 0;
  max-height: 100%;
  max-width: 100%;
}
.option-img:hover{
  box-shadow: 0 2px 0 0 rgb(204, 12, 57 / 50 ) inset;
  transition: all 0.2s ease;
}

.option-img-check-label {
  position: relative;
}
.option-img-check-label input{
  position: absolute;
  z-index: -1;
  opacity: 0;
}
.low.active, .mid.active, .high.active,
.option-img-check-label input:checked ~ .option-img{
  border: 1px solid #0F1111;
  transition: all 0.2s ease;
}

.option-img-check-label input:disabled ~ .option-img{
  //pointer-events: none;
  cursor: not-allowed;
  opacity: 50%;
  color: transparent !important;
}

/////////////////////////////////////////////////////////////////////

// Rise-pickers classes

.low{
  background-image: $option-rise-pickers-background-img;
  background-position: 0px 0px;
}
.mid{
  background-image: $option-rise-pickers-background-img;
  background-position: -100px 0px;
}
.high{
  background-image: $option-rise-pickers-background-img;
  background-position: -200px 0px;
}

</style>