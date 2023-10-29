<template>

  <ul class="customer-info-details">

    <li>
      <div class="row row-cols-auto ms-0 me-0 pt-3 clearfix">

        <div class="col-md-6 mb-3 ps-0 pe-1">

          <maz-input label="First name"
                     type="text"
                     v-model="info['firstName']"
                     color="black"
                     :required="inputs['firstName'].isRequired"
                     :auto-focus="props.autoFocus"
                     no-radius
                     @input="inputs['firstName'].isValid = isValidInput('firstName', $event.target.value)"
                     @change="setDetailValue('firstName', $event.target.value)"
                     :success="inputs['firstName'].isValid"
                     :error="inputs['firstName'].isValid === false ? true : null"
                     :hint="inputs['firstName'].isValid === false ? inputs['firstName'].hint : null"
                     autocomplete="given-name"
          />

        </div>

        <div class="col-md-6 mb-3 pe-1 related-field">

          <maz-input label="Last name"
                     type="text"
                     class="related-field-input"
                     v-model="info['lastName']"
                     color="black"
                     :required="inputs['lastName'].isRequired"
                     no-radius
                     @input="inputs['lastName'].isValid = isValidInput('lastName', $event.target.value)"
                     @change="setDetailValue('lastName', $event.target.value)"
                     :success="inputs['lastName'].isValid"
                     :error="inputs['lastName'].isValid === false ? true : null"
                     :hint="inputs['lastName'].isValid === false ? inputs['lastName'].hint : null"
                     autocomplete="family-name"
          />

        </div>

      </div>
    </li>

    <li v-if="!isBillingAddress">

      <div class="row ms-0 me-0 clearfix">
        <div class="col-md-12 mb-3 ps-0 pe-1">

          <maz-input label="Email"
                     type="email"
                     v-model="info['email']"
                     color="black"
                     :required="inputs['email'].isRequired"
                     no-radius
                     @input="inputs['email'].isValid = isValidInput('email', $event.target.value)"
                     @change="setDetailValue('email', $event.target.value)"
                     :success="inputs['email'].isValid"
                     :error="inputs['email'].isValid === false ? true : null"
                     :hint="inputs['email'].isValid === false ? inputs['email'].hint : null"
                     autocomplete="email"
          />

        </div>
      </div>

    </li>

    <li>
      <div class="row ms-0 me-0 clearfix">
        <div class="col-md-12 mb-3 ps-0 pe-1">

          <maz-phone-number-input v-model="info['phoneNumber']"
                                  color="black"
                                  :required="inputs['phoneNumber'].isRequired"
                                  no-radius
                                  @update="inputs['phoneNumber']['details'] = $event"
                                  @update:model-value="setDetailValue('phoneNumber', $event)"
                                  :success="inputs['phoneNumber']['details'].isValid"
                                  :translations="{
                                                phoneInput: {
                                                  placeholder: 'Phone number',
                                                  example: 'e.g. ',
                                                },
                                            }"
                                  :preferred-countries="['IQ']"
                                  autocomplete="tel"
          />

        </div>
      </div>
    </li>

    <li>
      <div class="row ms-0 me-0 clearfix">
        <div class="col-md-12 mb-3 ps-0 pe-1">

          <maz-input label="Address 1"
                     type="text"
                     v-model="info['address1']"
                     color="black"
                     :required="inputs['address1'].isRequired"
                     no-radius
                     @input="inputs['address1'].isValid = isValidInput('address1', $event.target.value)"
                     @change="setDetailValue('address1', $event.target.value)"
                     :success="inputs['address1'].isValid"
                     :error="inputs['address1'].isValid === false ? true : null"
                     :hint="inputs['address1'].isValid === false ? inputs['address1'].hint : null"
                     autocomplete="address-line1"
          />

        </div>
      </div>
    </li>

    <li>
      <div class="row ms-0 me-0 clearfix">
        <div class="col-md-12 mb-3 ps-0 pe-1">

          <maz-input label="Address 2"
                     type="text"
                     v-model="info['address2']"
                     color="black"
                     :required="inputs['address2'].isRequired"
                     no-radius
                     @input="inputs['address2'].isValid = isValidInput('address2', $event.target.value)"
                     @change="setDetailValue('address2', $event.target.value)"
                     :success="inputs['address2'].isValid"
                     :error="inputs['address2'].isValid === false ? true : null"
                     :hint="inputs['address2'].isValid === false ? inputs['address2'].hint : null"
                     autocomplete="address-line2"
          />

        </div>
      </div>
    </li>

    <li>
      <div class="row row-cols-auto ms-0 me-0 clearfix">

        <div class="col-md-6 mb-3 pe-1 ps-0">

          <maz-select label="Country"
                      type="text"
                      v-model="info['country']"
                      :options="inputs['country']['options']"
                      color="black"
                      :required="inputs['country'].isRequired"
                      no-radius
                      search
                      @update:model-value="($event) => {
                        setDetailValue('country', $event);
                      }"
          />

        </div>

        <div class="col-md-6 mb-3 pe-1 related-field">

          <maz-input label="Region"
                     type="text"
                     v-model="info['region']"
                     color="black"
                     :required="inputs['region'].isRequired"
                     no-radius
                     @input="inputs['region'].isValid = isValidInput('region', $event.target.value)"
                     @change="setDetailValue('region', $event.target.value)"
                     :success="inputs['region'].isValid"
                     :error="inputs['region'].isValid === false ? true : null"
                     :hint="inputs['region'].isValid === false ? inputs['region'].hint : null"
                     autocomplete="city"
          />

        </div>

      </div>
    </li>

    <li>
      <div class="row row-cols-auto ms-0 me-0 clearfix">

        <div class="col-md-6 mb-3 ps-0 pe-1">

          <maz-input label="City"
                     type="text"
                     v-model="info['city']"
                     color="black"
                     :required="inputs['city'].isRequired"
                     no-radius
                     @input="inputs['city'].isValid = isValidInput('city', $event.target.value)"
                     @change="setDetailValue('city', $event.target.value)"
                     :success="inputs['city'].isValid"
                     :error="inputs['city'].isValid === false ? true : null"
                     :hint="inputs['city'].isValid === false ? inputs['city'].hint : null"
                     autocomplete="city"
          />

        </div>

        <div class="col-md-6 mb-3 pe-1 related-field">

          <maz-input label="Postal code"
                     type="text"
                     v-model="info['postalCode']"
                     color="black"
                     :required="inputs['postalCode'].isRequired"
                     no-radius
                     @input="inputs['postalCode'].isValid = isValidInput('postalCode', $event.target.value)"
                     @change="setDetailValue('postalCode', $event.target.value)"
                     :success="inputs['postalCode'].isValid"
                     :error="inputs['postalCode'].isValid === false ? true : null"
                     :hint="inputs['postalCode'].isValid === false ? inputs['postalCode'].hint : null"
                     autocomplete="postal-code"
          />

        </div>

      </div>
    </li>

  </ul>

</template>

<script>

/*
   Info: if you want to add valid-button property to your maz input, add:

         :valid-button="inputs['firstName'].isValid"
 */

/*
   Info: maz phone number input has:
         1- @update event: triggered when component is updated or mounted and when country code input
                           or phone number input is changed, the $event will contain multiple variables.
         2- @update:model-value: triggered only phone number input is changed, the $event will contain
                                 the current value of phone number and will be in international form if
                                 it's valid.
         3- @country-code: the same as first but $event will be selected country code.

 */

/*
  Libraries, methods, variables and components imports
*/
import {ref, defineProps, defineEmits, watch, onMounted, onBeforeMount} from "vue";
// import {countries} from "@/common/countryListISOCodes";

export default {
  name: "MazDetailsInfoForm"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  details: {
    type: Object,
    // Object or array defaults must be returned from a factory function.
    // The function receives the raw props received by the component as the argument.
    default(rawProps) {
      return {}
    }
  },
  setDetailsMethod: {
    type: Function,
    required: true
  },
  countries: {
    type: Array,
    default(rawProps) {
      return [{label: '', value: ''}]
    }
  },
  isBillingAddress: {
    type: Boolean,
    default: false
  },
  autoFocus: {
    type: Boolean,
    default: true
  }
});
const info = ref(props.details);
const inputs = ref({});
// Define the list of events that you want to emit.
const emits = defineEmits(['isValid', 'isRequiredSet']);
// Regex formats, first () is to specify min and max characters while second () is for format.
const namesFormat = /(?=^.{0,50}$)(^[A-Za-z]*$)/;
const emailFormat = /(?=^.{0,255}$)(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$)/;
const addressFormat = /(?=^.{0,100}$)(^[#/.0-9a-zA-Z\s,-]+$)/;
const postalCodeFormat = /(^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$)/;
/* Regex for postal code should cover:
   1- Every postal code system uses only A-Z and/or 0-9 and sometimes space/dash
   2- Not every country uses postal codes (ex. Ireland outside of Dublin), but we'll ignore that here.
   3- The shortest postal code format is Sierra Leone with NN
   4- The longest is American Samoa with NNNNN-NNNNNN
   5- You should allow one space or dash.
   6- Should not begin or end with space or dash
 */

// Reference to access DOM element by using it with ref attribute.
// const firstName = ref(null);
// const lastName = ref(null);
// const email = ref(null);
// const phoneNumber = ref(null);
// const address1 = ref(null);
// const address2 = ref(null);
// const country = ref(null);
// const region = ref(null);
// const city = ref(null);
// const postalCode = ref(null);

/*
  Define functions
*/
const isValidInput = (inputName, val) => {
  /**
   * Method to set 'isValid' property of certain 'inputs' key.
   */

  let valid = null;

  if (![null, undefined, ''].includes(val)) {

    if (inputName === 'email') {
      valid = emailFormat.test(val);
    }
    else if (inputName === 'postalCode'){
      valid = postalCodeFormat.test(val);
    }
    else if (['address1', 'address2'].includes(inputName)){
      valid = addressFormat.test(val);
    }
    else {
      valid = namesFormat.test(val);
    }

  }
  return valid;
};
const setDetailValue = async (key, val) =>{
  /**
   * Method to set detail info key: value
   */

  if (key === 'phoneNumber' && inputs.value['phoneNumber']['details'].isValid === false) {
    return false
  }
  else if(inputs.value[key].isValid === false){
    return false
  }
  // In case everything is ok, set detail info value in the store.
  await props.setDetailsMethod(key, val);
};
const isValidForm = () => {
  /**
   * Return true if form inputs is set correctly and all required inputs are set, otherwise return false.
   */

  // Loop over 'inputs'
  for (let key of Object.keys(inputs.value)) {

    // Check that if current inputs key is required.
    if (inputs.value[key].isRequired === true) {

      // Check if its value is null/undefined or empty string.
      if ([undefined, null, ''].includes(info.value[key])) {
        // Emits a false value for 'isRequiredSet' event.
        emits('isRequiredSet', false);
        // No need to continue the loop.
        return
      }
      else {
        // Check if current key is 'phoneNumber' and its 'isValid' isn't true.
        if (key === 'phoneNumber' && [false, null].includes(inputs.value['phoneNumber']['details'].isValid)) {
          // Emits 'isValid' event with false value.
          emits('isValid', false);
          // No need to continue the loop.
          return
        }
        // In case current key isn't 'phoneNumber', check it's 'isValid' value.
        else if ([false, null].includes(inputs.value[key].isValid)) {
          // Emits 'isValid' event with false value.
          emits('isValid', false);
          // No need to continue the loop.
          return
        }
      }
    }
    // In case current input key isn't required but has invalid value.
    else if (![undefined, null, ''].includes(info.value[key]) && [false, null].includes(inputs.value[key].isValid)) {
      // Emits 'isValid' event with false value.
      emits('isValid', false);
      // No need to continue the loop.
      return
    }
  }

  // In case everything pass ok, emits the required events with true value.
  emits('isRequiredSet', true);
  emits('isValid', true);

};

// life-cycles

// Note: we can't access methods at initialize time because these methods could be not initialized yet.
onBeforeMount(() => {

  // Set 'inputs' properties
  // Note: Don't set value attribute, because we use v-model to set/get value of the input depending on
  //       'info' object.
  inputs.value = {
    firstName: {
      isValid: isValidInput('firstName', info.value['firstName']),
      isRequired: true,
      hint: 'Wrong, e.g. John'
    },
    lastName: {
      isValid: isValidInput('lastName', info.value['lastName']),
      isRequired: true,
      hint: 'Wrong, e.g. Doe'
    },
    phoneNumber: {
      isRequired: true,
      details: {}
    },
    address1: {
      isValid: isValidInput('address1', info.value['address1']),
      isRequired: true,
      hint: 'Wrong, e.g, 13, Main Str.'
    },
    address2: {
      isValid: isValidInput('address2', info.value['address2']),
      isRequired: false,
      hint: 'Wrong, e.g, Apt/Suite/Building'
    },
    country: {
      isValid: true,
      isRequired: true,
      options: props.countries
    },
    region: {
      isValid: isValidInput('region', info.value['region']),
      isRequired: true,
      hint: 'Wrong, State or Province'
    },
    city: {
      isValid: isValidInput('city', info.value['city']),
      isRequired: true,
      hint: 'Wrong, City name'
    },
    postalCode: {
      isValid: isValidInput('postalCode', info.value['postalCode']),
      isRequired: false,
      hint: 'Wrong, Postal or zip code'
    }
  };

  // Check if 'isBillingAddress' set to false, then add email input with its properties.
  if(props.isBillingAddress === false){
    inputs.value['email'] = {
      isValid: isValidInput('email', info.value['email']),
      isRequired: true,
      hint: 'Wrong, e.g. John.Doe@xyz.com'
    }
  }
});

onMounted(() => {

  // Trigger 'isValidForm' method the moment template is mounted.
  isValidForm();

  // Watch inputs
  // Note: we can't configure watch method outside onMounted() because we are configuring 'inputs'
  //       onBeforeMount step also, so will lead to trigger watch method twice when load component.
  watch(() => inputs.value, (currentValue, oldValue) =>
      {
        isValidForm();
      },
      {
        deep: true
      }
  );
})

</script>

<style lang="scss" scoped>

$main-color: #0F1111;

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}

.customer-info-details{
  list-style: none;
  padding-top: 8px;
  padding-left: 0;
}

hr{
    margin-top: 2rem;
}

.m-phone-number-input__input{
  width: 100%!important;
}

// for phones and tablets
@media(max-width:767px){
  .related-field{
    padding-left: 0!important;
  }
  input::placeholder {
    font-size: 12px;
  }
  //.m-phone-number-input{
  //  display: block!important;
  //}
  //.m-phone-number-input__country-flag{
  //  margin-bottom: 58px!important;
  //}
  //.m-phone-number-input__select{
  //  display: inline-block!important;
  //}
  //.m-phone-number-input__input{
  //  display: inline-block!important;
  //  margin-left: 2px!important;
  //  margin-top: 8px!important;
  //}
}
// for big screens
@media(min-width:768px) {
  .related-field {
    padding-left: 10px !important;
  }
}

</style>

<style lang="scss">

//label, option {
//  font-size: 14px;
//}
//input::placeholder {
//  font-size: 13px;
//}

</style>
