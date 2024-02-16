<template>

    <div v-for="( attribute ) in props.data"
         :key="whiteSpacesReplace(attribute.title, '-')"
         class="row pt-3"
    >
      <template v-if="attribute.options.length">

        <span class="attribute">{{ attribute.title }}</span>

        <template v-if="lowerCase(attribute.input_class) === 'option-btn'">

          <div class="row mt-1 pe-0">

            <div class="row row-cols-auto mt-1 pe-0" style="margin-left: 0">

              <div v-for="( option ) in attribute.options"
                   :key="whiteSpacesReplace(lowerCase(option), '-')"
                   class="col ps-0 pe-1"
              >

                <label :for="whiteSpacesReplace(lowerCase(option), '-')"
                       class="option-btn-check-label">
                  <input type="checkbox"
                         class="check-input"
                         v-model="checkInputs"
                         :id="whiteSpacesReplace(lowerCase(option), '-')"
                         :name="whiteSpacesReplace(lowerCase(option), '-')"
                         :value="option"
                  />

                  <span class="btn option-btn">{{ option }}</span>
                </label>

              </div>

            </div>

          </div>

        </template>

        <template v-else-if="lowerCase(attribute.input_class) === 'option-color'">

          <div class="row-cols-auto mt-1">

            <label v-for="( option ) in attribute.options"
                   :key="whiteSpacesReplace(lowerCase(option), '-')"
                   :for="whiteSpacesReplace(lowerCase(option), '-')"
                   v-tooltip
                   data-bs-toggle="tooltip"
                   data-bs-placement="top"
                   :title="option"
                   class="option-color-check-label"
            >
              <input type="checkbox"
                     v-model="checkInputs"
                     :id="whiteSpacesReplace(lowerCase(option), '-')"
                     :name="whiteSpacesReplace(lowerCase(option), '-')"
                     :value="option"
              />
              <span
                  :class="[
                      'option-color',
                      'col',
                      whiteSpacesReplace(lowerCase(option), '-')
                  ]"
              ><font-awesome-icon
                  v-if="!props.availableColorOptions.includes(whiteSpacesReplace(lowerCase(option)))"
                  icon="fa-solid fa-circle-check"/>
              </span>

            </label>

          </div>

        </template>

        <template v-else-if="lowerCase(attribute.input_class) === 'option-rise-picker'">

          <div class="row-cols-auto mt-1">

            <label v-for="( option ) in attribute.options"
                   :key="whiteSpacesReplace(lowerCase(option), '-')"
                   :for="whiteSpacesReplace(lowerCase(option), '-')"
                   v-tooltip
                   data-bs-toggle="tooltip"
                   data-bs-placement="top"
                   :title="option"
                   class="option-rise-picker-check-label"
            >
              <input type="checkbox"
                     v-model="checkInputs"
                     :id="whiteSpacesReplace(lowerCase(option), '-')"
                     :name="whiteSpacesReplace(lowerCase(option), '-')"
                     :value="option"
              />
              <span :class="['option-rise-picker col', whiteSpacesReplace(lowerCase(option), '-')]"></span>

            </label>

          </div>

        </template>

        <template v-else>

          <div class="row mt-1">

            <div v-for="( option ) in attribute.options"
                 :key="whiteSpacesReplace(lowerCase(option), '-')"
                 class="col-md-12 pt-1"
            >

              <label :for="whiteSpacesReplace(lowerCase(option), '-')"
                     class="form-check-label">
                <input type="checkbox"
                       class="form-check-input"
                       v-model="checkInputs"
                       :id="whiteSpacesReplace(lowerCase(option), '-')"
                       :name="whiteSpacesReplace(lowerCase(option), '-')"
                       :value="option"
                />
                <span>{{ option }}</span>
              </label>

            </div>

          </div>

        </template>
      </template>
    </div>


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import { MutationType } from 'pinia';
import {whiteSpacesReplacer} from "@/common/whiteSpacesReplacer";
// import {useRoute} from "vue-router";
import {watch, ref, toRef} from 'vue';

export default {
  name: "FilterAttributeComponent"
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
  data: {
    type: Array,
    required: true
  },
  checkedOptions: {
    type: Array,
    required: true
  },
  availableColorOptions: {
    type: [Array, undefined],
    required: false
  }
});
// const route = useRoute();
// const router = useRouter();
const storeFilter = toRef(props, 'storeFilter');
const checkInputs = ref(props.checkedOptions);

/*
  Define functions
*/
const lowerCase = (value) => {
  /**
   * Method to lower case any provided string.
   */
  // Note: you need to check if value is not none, otherwise will raise an exception undefined value.
  return value?.toLowerCase();
};
// const setColorStyle = (colorHex) => {
//   /**
//    * Method to return CSS string for <spain> of option-color class input.
//    */
//   return `background-color: #${colorHex};` +
//       'margin: 0 10px 5px 0.1px!important;' +
//       'width: 26px!important;' +
//       'height: 26px!important;'
// };
const whiteSpacesReplace = (str, use='') => {
  /**
   * Replace all whitespace in the string you need by use global mode (search
   * through whole string).
   */
  return whiteSpacesReplacer(str, use)
};

// const extractColorClass = (value) => {
//   /**
//    * Method use Regex to get a class name from value, matched:
//    * Blacks#eee blacks#eee Blacks #eee blacks #eee
//    *
//    */
//
//   let hashtagFormat = /#[a-e0-9_]{3,6}/;
//   let classNameFormat = /^[a-zA-Z]+[ #]/;
//   // hashtagFormat.test(value)
//
//   // Check if the length of returned array is contains only one item.
//   // Info: match() method will return null if no match is found.
//   let matchedArray = value.match(classNameFormat);
//   if( (matchedArray || []).length === 1 ){
//       return matchedArray[1]
//   }
//   else {
//     return value
//   }
//
// };

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
  /*
     Info: events key value of mutation in store is 'length' if the key related to array. But unfortunately
           events doesn't have attribute 'key' when and show 'Cannot read properties of undefined' error after
           build the code.
   */
  if ( [MutationType.direct].includes(mutation.type)) {
    checkInputs.value = state.checkedOptions;
  }

  // You can persist the whole state to the local storage whenever it changes.
  // localStorage.setItem('checkedOptions', JSON.stringify(state));

});

/*
  Watch the value of 'checkInputs', don't have to be immediate because its depend on user input.
  Info: watch() triggered when the related component is mount (if immediate property is
        set true) and unmount (if it defined inside setup life cycle directly) or
        watched value changed.
 */
watch(() => [...checkInputs.value], (currentValue, oldValue) =>
    {
      // Since we are watching value, this could cause a loop if you send
      // patch signal and then receive same signal to update your data.

      if (currentValue.length !== oldValue.length) {

        storeFilter.value.$patch({
          checkedOptions: currentValue
        });

      }
    },
);

</script>

<style scoped lang="scss">

$option-colors-background-img: url("../assets/images/swatches/softlines-colors.png");
$option-rise-pickers-background-img: url("../assets/images/swatches/rise-pickers.png");

.attribute {
  line-height: 16px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
}

div.scrollmenu {
  overflow: auto;
  white-space: nowrap;
}

div.scrollmenu::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
}

div.scrollmenu{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.form-check-label span:hover {
  transition: color 200ms ease-in-out;
  color: rgb(204, 12, 57) !important;
}

.form-check-input {
  margin-right: 5px;
}

//div.col:first-child {
//  padding-left: 11px !important;
//}
//
//div.col:not(:first-child) {
//  padding-left: 3px;
//  padding-right: 0;
//}

.option-btn {
  color: #464646 !important;
  letter-spacing: 1px;
  border-width: 1px;
  border-style: solid;
  border-color: #D5D9D9 !important;
  border-radius: 2px;
  box-shadow: 0 2px 5px 0 rgb(213 217 217 / 50 ) !important;
}

.option-btn:hover {
  cursor: pointer;
  transition: color 200ms ease-in-out;
  background-color: #e9ecef !important;
  color: rgb(204, 12, 57) !important; // #CC0C39
}

.option-btn-check-label {
  position: relative;
}
.option-btn-check-label input {
  position: absolute;
  z-index: -1;
  opacity: 0;
}
.option-btn-check-label input:checked ~ .btn {
  transition: color 200ms ease-in-out;
  background-color: #0F1111 !important;
  color: #fff !important;
}
.option-btn-check-label input:disabled ~ .btn {
  pointer-events: none;
}

.option-color {
  height: 36px;
  width: 36px;
  background-size: 1700px 500px;
  margin: 0 5px 0 -5px;
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
  pointer-events: none;
}

.fa-circle-check{
  float: left;
  padding: 0;
  margin: 6px 0 0 5.5px ;
  font-size: 14px;
  font-style: normal;
  font-variant: normal;
  text-rendering: auto;
  -webkit-font-smoothing: antialiased;
  border-radius: 50%;
  background-color: #0F1111;
  color: #fff;
  opacity: -1;
}

.option-color-check-label input:checked ~ .option-color .fa-circle-check{
  opacity: 1;
}

.option-rise-picker{
  height: 49px;
  width: 44px;
  margin: 5px 6px 0 0;
  display: inline-block;
  cursor: pointer;
}
.option-rise-picker:hover{
  box-shadow: 0 2px 0 0 rgb(204, 12, 57) inset;
  transition: all 0.2s ease;
}

.option-rise-picker-check-label {
  position: relative;
}
.option-rise-picker-check-label input{
  position: absolute;
  z-index: -1;
  opacity: 0;
}
.low.active, .mid.active, .high.active,
.option-rise-picker-check-label input:checked ~ .option-rise-picker{
  border: 1px solid #0F1111;
  transition: all 0.2s ease;
}

.option-rise-picker-check-label input:disabled ~ .option-rise-picker{
  pointer-events: none;
}

// Color classes
.blacks {
  background-image: $option-colors-background-img;
  background-position: 0px 0px;
}

.greys {
  background-image: $option-colors-background-img;
  background-position: -100px 0px;
}

.white {
  background-image: $option-colors-background-img;
  background-position: -200px 0px;
}

.browns {
  background-image: $option-colors-background-img;
  background-position: -300px 0px;
}

.beige {
  background-image: $option-colors-background-img;
  background-position: -400px 0px;
}

.reds {
  background-image: $option-colors-background-img;
  background-position: -500px 0px;
}

.pinks {
  background-image: $option-colors-background-img;
  background-position: -600px 0px;
}

.oranges {
  background-image: $option-colors-background-img;
  background-position: -700px 0px;
}

.yellows {
  background-image: $option-colors-background-img;
  background-position: -800px 0px;
}

.ivory {
  background-image: $option-colors-background-img;
  background-position: -900px 0px;
}

.greens {
  background-image: $option-colors-background-img;
  background-position: -1000px 0px;
}

.blues {
  background-image: $option-colors-background-img;
  background-position: -1100px 0px;
}

.purples {
  background-image: $option-colors-background-img;
  background-position: -1200px 0px;
}

.golds {
  background-image: $option-colors-background-img;
  background-position: -1300px 0px;
}

.silvers {
  background-image: $option-colors-background-img;
  background-position: -1400px 0px;
}

.multi {
  background-image: $option-colors-background-img;
  background-position: -1500px 0px;
}

.clear {
  background-image: $option-colors-background-img;
  background-position: -1600px 0px;
}

//
// customized colors
.light-wash, .medium-wash, .dark-wash{
  margin: 0 10px 5px 0.1px!important;
  width: 26px!important;
  height: 26px!important;
}

.light-wash{
  background: #CBDAE9;
}

.medium-wash{
  background: #7C95B3;
}

.dark-wash{
  background: #3E5A7A;
}

//
// Color classes: Color classes.active
.blacks.active,
.option-color-check-label input:checked ~ .blacks{
  background-image: $option-colors-background-img;
  background-position: 0px -100px;
}

.greys.active,
.option-color-check-label input:checked ~ .greys{
  background-image: $option-colors-background-img;
  background-position: -100px -100px;
}

.white.active,
.option-color-check-label input:checked ~ .white{
  background-image: $option-colors-background-img;
  background-position: -200px -100px;
}

.browns.active,
.option-color-check-label input:checked ~ .browns{
  background-image: $option-colors-background-img;
  background-position: -300px -100px;
}

.beige.active,
.option-color-check-label input:checked ~ .beige{
  background-image: $option-colors-background-img;
  background-position: -400px -100px;
}

.reds.active,
.option-color-check-label input:checked ~ .reds{
  background-image: $option-colors-background-img;
  background-position: -500px -100px;
}

.pinks.active,
.option-color-check-label input:checked ~ .pinks{
  background-image: $option-colors-background-img;
  background-position: -600px -100px;
}

.oranges.active,
.option-color-check-label input:checked ~ .oranges{
  background-image: $option-colors-background-img;
  background-position: -700px -100px;
}

.yellows.active,
.option-color-check-label input:checked ~ .yellows{
  background-image: $option-colors-background-img;
  background-position: -800px -100px;
}

.ivory.active,
.option-color-check-label input:checked ~ .ivory{
  background-image: $option-colors-background-img;
  background-position: -900px -100px;
}

.greens.active,
.option-color-check-label input:checked ~ .greens{
  background-image: $option-colors-background-img;
  background-position: -1000px -100px;
}

.blues.active,
.option-color-check-label input:checked ~ .blues{
  background-image: $option-colors-background-img;
  background-position: -1100px -100px;
}

.purples.active,
.option-color-check-label input:checked ~ .purples{
  background-image: $option-colors-background-img;
  background-position: -1200px -100px;
}

.golds.active,
.option-color-check-label input:checked ~ .golds{
  background-image: $option-colors-background-img;
  background-position: -1300px -100px;
}

.silvers.active,
.option-color-check-label input:checked ~ .silvers{
  background-image: $option-colors-background-img;
  background-position: -1400px -100px;
}

.multi.active,
.option-color-check-label input:checked ~ .multi{
  background-image: $option-colors-background-img;
  background-position: -1500px -100px;
}

.clear.active,
.option-color-check-label input:checked ~ .clear{
  background-image: $option-colors-background-img;
  background-position: -1600px -100px;
}

//
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


// Rise-pickers classes hover
//.low:hover{
//  background-image: $option-rise-pickers-background-img;
//  background-position: 0px -100px;
//}
//.mid:hover{
//  background-image: $option-rise-pickers-background-img;
//  background-position: -100px -100px;
//}
//.high:hover{
//  background-image: $option-rise-pickers-background-img;
//  background-position: -200px -100px;
//}

// Rise-pickers classes.active
//.low.active,
//.option-rise--picker-check-label input:checked ~ .low{
//  background-image: $option-rise-pickers-background-img;
//  background-position: 0px -200px;
//}
//.mid.active,
//.option-rise--picker-check-label input:checked ~ .mid{
//  background-image: $option-rise-pickers-background-img;
//  background-position: -100px -200px;
//}
//.high.active,
//.option-rise--picker-check-label input:checked ~ .high{
//  background-image: $option-rise-pickers-background-img;
//  background-position: -200px -200px;
//}

</style>