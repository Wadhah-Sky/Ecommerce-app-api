<template>

  <div class='vnis'>

    <button @click='decreaseNumber'
            @mousedown='whileMouseDown(decreaseNumber)'
            @mouseup='clearTimer'
            :class='buttonClass'
            :disabled="numericValue <= props.min"
    >-
    </button>

    <input type="number"
           :value='numericValue'
           @input='validateInput($event.target)'
           :class='inputClass'
           :min='props.min'
           :max='props.max'
           :disabled="disabled"
           :pattern="`/^\d{${props.max}}$/`"
    />

    <button @click='increaseNumber'
            @mousedown='whileMouseDown(increaseNumber)'
            @mouseup='clearTimer'
            :class='buttonClass'
            :disabled="numericValue >= props.max"
    >+
    </button>

  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import{ref, defineProps, defineEmits, watch} from "vue";

export default {
  name: "NumberInputSpinnerComponent"
}
</script>

<script setup>
/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  value: {
    type: Number
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 10
  },
  step: {
    // The increase/decrease value.
    type: Number,
    default: 1
  },
  mouseDownSpeed: {
    // mouseDown event speed (in milliseconds).
    type: Number,
    default: 500
  },
  inputClass: {
    type: String,
    default: 'vnis__input'
  },
  buttonClass: {
    type: String,
    default: 'vnis__button'
  },
  integerOnly: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
});
// Set numeric value as same as the provided 'props.value' or in case it's not provided, use the 'props.min'
const numericValue = ref(props.value || props.min);
const timer = ref(null);
// Define the list of events that you want to emit.
const emits = defineEmits(['input']);

/*
  Define functions
*/
/*
 Note: when the user click on the (+) or (-) buttons, will tigger the following:
       1- whileMouseDown() with callback method.
       2- the callback method.
       3- clear() method (keyup event).
*/
const whileMouseDown = (callback) => {
  /**
   * Method to tigger setInterval() method given a callback method to be triggered continuously in
   * certain time (milliseconds) when a user presses a mouse button over an HTML element.
   */
  // Check that 'timer' is null.
  if (timer.value === null) {
    // Set 'timer' value using setInterval() method to trigger certain method continuously in certain time (milliseconds).
    timer.value = setInterval(() => {callback();}, props.mouseDownSpeed);
  }
};
const clearTimer = () => {
  /**
   * Method to clear (stop) a certain timer that have set by setInterval() method.
   */
  // check that the current 'timer' is not a null.
  if (timer.value) {
    // The clearInterval() method clears (stop) a timer set with the setInterval() method.
    clearInterval(timer.value);
    // Re-set the 'timer' value.
    timer.value = null;
  }
};
const increaseNumber = () =>{
  /**
   * Method to increase the value of 'numericValue' depending on 'step' value.
   */
  numericValue.value += props.step;
};
const decreaseNumber = () =>{
  /**
   * Method to decrease the value of 'numericValue' depending on 'step' value.
   */
  numericValue.value -= props.step;
};
const isInteger = (e) => {
  /**
   * Method to check value of certain input, it's integer otherwise set current
   * input value to be the same as the provided 'min' value.
   */

  /*
    Note: 1- The event.which (non-standard) property returns which keyboard key or mouse button was pressed for
             the event.
          2- The event.keyCode (Deprecated) read-only property represents a system and implementation dependent
             numerical code identifying the unmodified value of the pressed key.
   */
  // let key = e.keyCode || e.which;

  // The static String.fromCharCode() method returns a string created from the specified sequence of UTF-16 code units.
  // key = String.fromCharCode(key);

  // Get value of input.
  let val = e.value;

  // Regex of only integer numbers (negative and positive) to tests input value against.
  const regex = /[0-9]/g;

  // If 'key' value pass the tests() method of 'regex' value.
  if (regex.test(val)) {
    return true;
  }
  else {
    /*
         Info: The preventDefault() method of the Event interface tells the user agent that if the event
               does not get explicitly handled, its default action should not be taken as it normally would be.
               In other words, stop the input from set the given value by user as its value.

               Note: this property not working with vue.js, and it's similar to @submit.prevent
       */
    // e.preventDefault();

    // Set current input value to be the same as the provided 'min' value.
    e.value = props.min;

    return false;
  }
};
const isNumber = (e) =>{
  /**
   * Method to check value of certain input, it's number otherwise set current
   * input value to be the same as the provided 'min' value.
   */

  // Remember: isNaN() works only with string/number/integer, if provide an empty value will return false.
  if(isNaN(e.value)){
    /*
         Info: The preventDefault() method of the Event interface tells the user agent that if the event
               does not get explicitly handled, its default action should not be taken as it normally would be.
               In other words, stop the input from set the given value by user as its value.

               Note: this property not working with vue.js, and it's similar to @submit.prevent
       */
    // e.preventDefault();

    // Set current input value to be the same as the provided 'min' value.
    e.value = props.min;

    return false;
  }
  else {
    return true;
  }
};
const validateInput = (e) => {
  /**
   * Method to validate the value of input.
   */

  if (props.integerOnly === true){
    isInteger(e);
  }
  else {
    isNumber(e);
  }

  // Tigger the 'setNumericValue';
  setNumericValue(e);

};
const setNumericValue = (e) => {
  /**
   * Method to set value of 'numericValue' depending on value certain input.
   */

  // Set event's input value if exists otherwise set 'props.min' as value of 'numericValue'.
  numericValue.value = e.value ? parseInt(e.value) : props.min;
};

// Watch 'numericValue'
watch(() => numericValue.value, (currentValue, oldValue) =>
    {
      if (currentValue <= props.min) {
        numericValue.value = parseInt(props.min);
      }
      if (currentValue >= props.max) {
        numericValue.value = parseInt(props.max);
      }
      if (currentValue <= props.max && currentValue >= props.min) {
        emits('input', {currentValue: currentValue, oldValue: oldValue });
      }
    },
);

</script>

<style scoped lang="scss">

.vnis {
  *,
  *::after,
  *::before {
    box-sizing: border-box;
  }
  &__input {
    -webkit-appearance: none;
    border: 1px solid #ebebeb;
    font-weight: 400;
    float: left;
    font-size: 14px;
    color: #0f1111;
    height: 20px;
    margin: 0;
    outline: none;
    text-align: center;
    max-width: calc(90% - 50px);
    &::-webkit-outer-spin-button,
    &::-webkit-inner-spin-button {
      -webkit-appearance: none;
    }
  }
  &__button {
    -webkit-appearance: none;
    transition: background 0.5s ease;
    background: #0f1111;
    border: 0;
    color: #fff;
    cursor: pointer;
    float: left;
    font-size: 14px;
    font-weight: 400;
    height: 20px;
    text-align: justify-all;
    padding: 0;
    margin: 0;
    width: 20px;
    &:hover {
      background: lighten(#0f1111, 10%);
    }
    &:focus {
      //outline: 1px dashed lighten(#0f1111, 20%);
      outline-offset: -5px;
    }
    &:disabled {
      color: #464646;
      background-color: #e9ecef;
      cursor: no-drop;
    }
  }
}

</style>