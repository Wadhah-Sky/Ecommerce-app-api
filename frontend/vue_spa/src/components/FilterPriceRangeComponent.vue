<template>

  <div class="row mt-1" style="padding-right: 0; margin-right: 0;">

    <ul class="list-group">
      <li class="list-group-item" @click="updateInputsAndSubmit(1, 25)" >Up to $25</li>
      <li class="list-group-item" @click="updateInputsAndSubmit(25, 50)" >$25 to $50</li>
      <li class="list-group-item" @click="updateInputsAndSubmit(50, 100)" >$50 to $100</li>
      <li class="list-group-item" @click="updateInputsAndSubmit(100, 200)" >$100 to $200</li>
      <li class="list-group-item" @click="updateInputsAndSubmit(200, undefined)" >$200 & above</li>
    </ul>

    <form class="row row-cols-auto needs-validation" novalidate @submit.prevent >

      <div class="col ms-2 pe-0 position-relative">

        <div class="input-group">

          <span class="input-group-text" id="basic-addon1">$</span>
          <input v-tooltip
                 :ref="minPriceInput.el"
                 v-imask="minPriceInput.mask"
                 type="number"
                 id="low-price"
                 class="form-control"
                 data-bs-toggle="tooltip"
                 data-bs-placement="top"
                 title="Enter min price"
                 name="low-price"
                 placeholder="Min"
                 pattern="/^\d{4}$/"
                 maxlength="4"
                 min="0"
                 max="4999"
        />

        </div>

      </div>

      <div class="col position-relative" style="padding-right: 0; margin-right: 0">

        <div class="input-group">

          <span class="input-group-text" id="basic-addon2">$</span>
          <input v-tooltip
                 :ref="maxPriceInput.el"
                 v-imask="maxPriceInput.mask"
                 type="number"
                 id="high-price"
                 class="form-control"
                 data-bs-toggle="tooltip"
                 data-bs-placement="bottom"
                 :title="maxMsg.normalMsg"
                 name="high-price"
                 placeholder="Max"
                 pattern="/^\d{4}$/"
                 maxlength="4"
                 min="1"
                 max="5000"
                 @complete="maxError ? maxError = false : ''"
          />

        </div>

      </div>

      <div class="col position-relative" style="padding-right: 0!important;">
        <label for="submit-price" id="submit-btn-label">
          <input type="submit"
                 id="submit-price"
                 @click="submitPriceRange"
          />
          <span id="submit-btn" class="btn">Go</span>
        </label>
      </div>

      <div v-show="maxError"
           class="row mt-2 ms-2 me-0 pe-0 alert alert-secondary"
           role="alert" style="padding: 0; margin: 0"
      >
        <div class="col">

          <span class="alert-msg">{{maxMsg.errorMsg}}</span>

        </div>

      </div>

    </form>

  </div>

</template>

<script>

/*
  You can use:

  1- Attributes for min price <input> element:
     pattern="/^\d{4}$/" maxlength="4" min="0" max="4999"

  2- Attributes for max price <input> element:
     pattern="/^\d{4}$/" maxlength="4" min="1" max="5000"

  Note: Max-length and min and max works only with spinner (when using
        keyboard up and down buttons)

  Info: You can use directive @input to handle any event with inputs field and
        can call your handle function by sending $event:

        <input type-"number" @input="checkNumberFieldMinValue($event)" />

        In you function handle you can access the event target and its value:

        const checkNumberFieldMinValue = (ele) => { ele.target.value }

        or you can use directive :v-model.number='<ref_name>' and handle it from a method
        when the input changed/clicked or even watch the ref.
 */

/*
  Libraries, methods, variables and components imports
*/
// import {querySerializer} from "@/common/querySerializer";
import { MutationType } from 'pinia';
import {minPriceProps, maxPriceProps} from "@/common/inputMask";
import {useRoute} from "vue-router";
import {ref, toRef, defineProps, onMounted} from 'vue';

export default {
  name: "FilterPriceRangeComponent"
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
  minPrice: {
    type: [String, Number, undefined],
    required: false
  },
  maxPrice: {
    type: [String, Number, undefined],
    required: false
  }
});
const storeFilter = toRef(props, 'storeFilter');
// const priceObj = ref({
//   'minPrice': props.minPrice,
//   'maxPrice': props.maxPrice
// });
// const router = useRouter();
const route = useRoute();
const maxError = ref(false);
const maxMsg = ref(
    {
      normalMsg: 'Enter max price',
      errorMsg: 'max price should be bigger than min price'
    }
);
// Note: <ref_name>.value represent the element itself, to get its value use <ref_name>.value.value
const minPriceInput = {
  el: ref(null),
  mask: minPriceProps,
  isRequired: true,
};
const maxPriceInput = {
  el: ref(null),
  mask: maxPriceProps,
  isRequired: true,
};

/*
  Define functions
*/
const updateInputs = (minVal, maxVal) => {
  /**
   * Update values of input min and max
   */

  if ([undefined, '', null]. includes(minVal)){
    minPriceInput.el.value.value = '';
  }
  else {
    minPriceInput.el.value.value = minVal;
  }

  if ([undefined, '', null]. includes(maxVal)){
    maxPriceInput.el.value.value = '';
  }
  else {
    maxPriceInput.el.value.value = maxVal;
  }
};
const submitPriceRange = () => {
  /**
   * Method to submit price range after validation.
   */

  // Info: we allow submitting to push undefined values (empty) because in case you have set value and the then
  //       delete it, it's possible to reset it, even if min and max inputs both are empty.

  // Note: default value of minVal and maxVal is undefined, if you use +minVal will change to 0 because
  //       it's default value for Type Number

  // Get min and max input values.
  let minVal = minPriceInput.el.value.value;
  let maxVal = maxPriceInput.el.value.value;

  // Get route query values of min and max price (if not defined will return 'undefined')
  let routeQueryMinPrice = +route.query.minPrice;
  let routeQueryMaxPrice = +route.query.maxPrice;

  // Initialize default price object
  let priceObj = {minPrice: undefined, maxPrice: undefined};

  // Initialize flag to determine to update store or not
  let updateStore = false;

  // in case both of minVal and maxVal is set as Number value type, check if minVal is bigger than maxVal?
  /*
     Note: Don't use the following way because it's not guarantee:

           typeof minVal === "number"

           Use regex way:

           /^[0-9]+[.]{0,1}[0-9]*$/.test(<value>)

           1- /^ : Refers to start your string
           2- $/ : Refers to end of your string
           3- [0-9]+ : Starting of string is from 0 to 9 with minimum one length
           4- [.]{0,1} : Can contain 0 or at max 1 '.'
           5- [0-9]* : Can contain 0 to 9 digits at the end of string.
   */
  if ( /^[0-9]+[.]{0,1}[0-9]*$/.test(minVal) && /^[0-9]+[.]{0,1}[0-9]*$/.test(maxVal) && (+minVal > +maxVal) ) {
    maxError.value = true;
    maxPriceInput.el.value.focus();
  }

  // In case the current value of minVal and maxVal are valid and active in url, don't update store values.
  if ((minVal !== undefined) && (+minVal !== routeQueryMinPrice)){
    priceObj['minPrice'] = minVal;
    updateStore = true;
  }

  if ((maxVal !== undefined) && (+maxVal !== routeQueryMaxPrice)){
    priceObj['maxPrice'] = maxVal;
    updateStore = true;
  }

  // In case the update store flag is true.
  if(updateStore){
    // How to use serializedQueryObj method:
    // let serializedQueryObj = querySerializer(priceObj.value, route.query, [0, null, undefined]);

    // Change state of price object in filter store using patch way because it's been watch to push new route
    // state in storeCategory view.
    storeFilter.value.$patch({
      price: {minPrice: minVal, maxPrice: maxVal}
    });
  }

};
const updateInputsAndSubmit = (minVal, maxVal) => {
  /**
   * Calling update inputs method and submit new value of min and max price.
   */
  updateInputs(minVal, maxVal);
  submitPriceRange();
};

// Life cycle
onMounted(() => {
  // Initialize values of input min and max.
  updateInputs(props.minPrice, props.maxPrice);
});

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
             your data in store, because this will lead to loop.
 */
storeFilter.value.$subscribe((mutation, state) => {
  // You can specify type of mutation.
  if ( [MutationType.direct].includes(mutation.type) && mutation.events.key === 'price' ) {
    updateInputs(state.price.minPrice, state.price.maxPrice);

    // submit price
    submitPriceRange();
  }

  // You can persist the whole state to the local storage whenever it changes.
  // localStorage.setItem('checkedOptions', JSON.stringify(state));

});

// Watch the selectedOption object.
// watch(() => priceObj.value, (currentValue, oldValue) =>
//     {
//       console.log("Push watch", currentValue, oldValue)
//       storeFilter.value.$patch({
//         price: currentValue,
//       });
//     },
//     {
//       deep: true
//     }
// );

// watchEffect(
//     () => {
//       console.log("Triggered", max.value)
//     },
//     {
//       flush: "post",
//     }
// )

</script>

<style scoped>

form{
  padding-right: 0;
  margin-right: 0;
  width: 100%;
}
.col{
  padding-left: 0;
}

.list-group-item{
  border: none;
  padding: 0;
  margin-right: 0;
  margin-left: 11px;
}

.list-group-item:hover{
  cursor: pointer;
  color: rgb(204, 12, 57);
  transform: translateX(3px);
  transition: all 0.3s ease;
}

#low-price, #high-price {
  border-color: #fff;
  height: 31px;
  padding: 3px 7px;
  line-height: normal;
  width: 69px;
  margin-top: 6px !important;
  margin-right: 1px;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}

#basic-addon1, #basic-addon2{
  font-size: 100%;
  outline: 0;
  padding: 1px 3px;
  height: 29px;
  margin-top: 7px;
  color: #fff;
  background-color: #0F1111;
}

input[type=number] {
  border: 1px solid #464646;
  border-radius: 3px;
  box-shadow: 0 0 1px 2px rgb(15 17 17 / 15%) inset;
  outline: 0;
  font-size: 100%;
  font-family: inherit;
}

input[type=number]:hover {
  box-shadow: 0 0 1px 2px #0F1111 inset;
  transition: color 0.3s ease;
}

input[type=number]:focus {
  box-shadow: 0 0 1px 2px #0F1111 inset;
  transition: color 0.3s ease;
}

#submit-btn {
  /*border: 1px solid #0F1111;*/
  box-shadow: 0 0 1px 2px rgb(15 17 17 / 15%) inset;
  height: 31px;
  padding: 3px 7px;
  line-height: normal;
  width: 35px;
  margin-top: 6px !important;
  margin-right: 0px;
}

#submit-btn:hover {
  cursor: pointer;
  transition: color 200ms ease-in-out;
  background-color: #0F1111 !important;
  color: #fff;
}

#submit-btn-label {
  position: relative;
}
#submit-btn-label input {
  position: absolute;
  z-index: -1;
  opacity: 0;
}

.alert-secondary{
  opacity: 80%;
  background-color: #fff;
  transition: all 0.3s ease;
}

.alert-msg{
  display: inline-block;
  margin: auto;
  color: rgb(204, 12, 57);
  font-size: 13px;
  font-weight: 400;
  text-align: center;
}

</style>