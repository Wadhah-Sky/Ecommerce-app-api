<template>

  <div class="row mt-1">

    <ul class="list-group">
      <li class="list-group-item" @click="setAndSubmitMinMaxPrice(1, 25)" >Up to $25</li>
      <li class="list-group-item" @click="setAndSubmitMinMaxPrice(25, 50)" >$25 to $50</li>
      <li class="list-group-item" @click="setAndSubmitMinMaxPrice(50, 100)" >$50 to $100</li>
      <li class="list-group-item" @click="setAndSubmitMinMaxPrice(100, 200)" >$100 to $200</li>
      <li class="list-group-item" @click="setAndSubmitMinMaxPrice(200, null)" >$200 & above</li>
    </ul>

    <form class="row row-cols-auto needs-validation" novalidate @submit.prevent >

      <div class="col ms-2 pe-0 position-relative">

        <div class="input-group">

          <span class="input-group-text" id="basic-addon1">$</span>
          <input v-tooltip
               type="number"
               v-model="priceObj.minPrice"
               ref="min"
               id="low-price"
               class="form-control"
               data-bs-toggle="tooltip"
               data-bs-placement="top"
               title="Enter min price"
               @input="validateMinPrice"
               pattern="/^\d{4}$/" maxlength="4" min="0" max="4999"
               name="low-price" placeholder="Min"
        />

        </div>

      </div>

      <div class="col position-relative">

        <div class="input-group">

          <span class="input-group-text" id="basic-addon2">$</span>
          <input v-tooltip
                 type="number"
                 v-model="priceObj.maxPrice"
                 ref="max"
                 id="high-price"
                 class="form-control"
                 data-bs-toggle="tooltip"
                 data-bs-placement="bottom"
                 :title="maxMsg.normalMsg"
                 @input="validateMaxPrice"
                 pattern="/^\d{4}$/" maxlength="4" min="1" max="5000"
                 name="high-price" placeholder="Max"
          />

        </div>


      </div>

      <div class="col position-relative">
        <label for="submit-price" id="submit-btn-label">
          <input type="submit"
                 id="submit-price"
                 @click="setAndSubmitMinMaxPrice(priceObj.minPrice, priceObj.maxPrice)"
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
  Libraries, methods, variables and components imports
*/
import {querySerializer} from "@/common/querySerializer";
import {useRoute, useRouter} from "vue-router";
import { MutationType } from 'pinia';
import {ref, toRef, defineProps} from 'vue';

export default {
  name: "PriceRangeComponent"
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
  }
});
const storeFilter = toRef(props, 'storeFilter');
const priceObj = ref({
  'minPrice': storeFilter.value.price['minPrice'],
  'maxPrice': storeFilter.value.price['maxPrice']
});
const router = useRouter();
const route = useRoute();
// Note: <ref_name>.value represent the element itself, to get its value use <ref_name>.value.value
const min = ref(null);
const max = ref(null)
const maxError = ref(false);
const maxMsg = ref(
    {
      normalMsg: 'Enter max price',
      errorMsg: 'max price should be bigger than min price'
    }
);
// const route = useRoute();

/*
  Define functions
*/
const validateMinPrice = () => {
  /**
   * Method to watch the direct input by user in Min number input field.
   *
   * Min value: 0 and Max value: 5000, and should be less than Max input field.
   *
   * Note: Max-length and min and max works only with spinner (when using
   * keyboard up and down buttons)
   */

  /*
    Info: You can use directive @input to handle any event with inputs field and
          can call your handle function by sending $event:

          <input type-"number" @input="checkNumberFieldMinValue($event)" />

          In you function handle you can access the event target and its value:

          const checkNumberFieldMinValue = (ele) => { ele.target.value }

          or you can use directive :v-model.number='<ref_name>' and handle it from a method
          when the input changed/clicked or even watch the ref.
   */

  // Set 'maxError' state to be false.
  maxError.value = false;

  if ( typeof priceObj.value.minPrice === "number" ) {
    // In case user entered negative value.
    let minVal = +priceObj.value.minPrice;
    if (+minVal < 0) {
      priceObj.value.minPrice = 0;
    } else if (+minVal >= 5000) {
      priceObj.value.minPrice = 4999;
    }
  }
  else {
    priceObj.value.minPrice = null;
  }
};
const validateMaxPrice = () => {
  /**
   * Method to watch the direct input by user in Max number input field.
   *
   * Min value: 0 and Max value: 5000, and should be bigger than Min input field.
   *
   * Note: Max-length and min and max works only with spinner (when using
   * keyboard up and down buttons)
   */

  /*
    Info: You can use directive @input to handle any event with inputs field and
          can call your handle function by sending $event:

          <input type-"number" @input="checkNumberFieldMaxValue($event)" />

          In you function handle you can access the event target and its value:

          const checkNumberFieldMaxValue = (ele) => { ele.target.value }

          or you can use directive :v-model.number='<ref_name>' and handle it from a method
          when the input changed/clicked or even watch the ref.
   */

  // Set 'maxError' state to be false.
  maxError.value = false;

  if ( typeof priceObj.value.maxPrice === "number") {
    // In case user entered negative value or zero.
    let maxVal = +priceObj.value.maxPrice;
    if (+maxVal < 0) {
      priceObj.value.maxPrice = 1;
    } else if (+maxVal > 5000) {
      priceObj.value.maxPrice = 5000
    }
  }
  else{
    priceObj.value.maxPrice = null;
  }


};
const setAndSubmitMinMaxPrice = (minVal, maxVal) => {
  /**
   * Method to set minPrice and maxPrice and trigger submit method.
   */

  // Set priceObj values.
  priceObj.value.minPrice = minVal;
  priceObj.value.maxPrice = maxVal;

  // Trigger submit method
  submitPriceRange(minVal, maxVal);
};
const submitPriceRange = (minVal=null, maxVal=null) => {
  /**
   * Method to submit price range after validation.
   */

  // in case both of minVal and maxVal is set, check if minVal is bigger than maxVal.
  if ((typeof minVal === "number" && typeof maxVal === "number") && (+minVal > +maxVal)) {
    maxError.value = true;
    max.value.focus();
  }
  // In case the current value of minVal and maxVal are active in url, don't push.
  else if ( !((+minVal === +route.query.minPrice) && (+maxVal === +route.query.maxPrice)) ) {

    // Get serializedQueryObj
    let serializedQueryObj = querySerializer(priceObj.value, route.query, [0, null]);

    // push new router state.
    router.push({
      path: route.path,
      query: {...serializedQueryObj, page: 1}
    });
  }
};

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

    priceObj.value.minPrice = state.price.minPrice;
    priceObj.value.maxPrice = state.price.maxPrice

    // Submit the new value of priceObj.
    submitPriceRange(priceObj.value.minPrice, priceObj.value.maxPrice);

  }

  // You can persist the whole state to the local storage whenever it changes.
  // localStorage.setItem('checkedOptions', JSON.stringify(state));

});

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
  transition: color 0.3s ease;
}

#low-price, #high-price {
  border-color: #fff;
  height: 31px;
  padding: 3px 7px;
  line-height: normal;
  width: 55px;
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
  width: 40px;
  margin-top: 6px !important;
  margin-right: 1px;
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
  background-color: #e9ecef;
  transition: all 0.3s ease;
}

.alert-msg{
  color: rgb(204, 12, 57);
  font-size: 13px;
  text-align: center;
}

</style>