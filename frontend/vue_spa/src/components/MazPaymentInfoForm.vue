<template>

  <ul class="payment-info-details">

    <li>
      <div class="row row-cols-auto ms-0 me-0 pt-3 clearfix">

        <div class="col-md-6 mb-3 ps-0 pe-1">

          <maz-select label="Payment method"
                      class="payment-method"
                      type="text"
                      v-model="info['paymentMethod']"
                      :options="inputs['paymentMethod']['options']"
                      :required="inputs['paymentMethod'].isRequired"
                      color="black"
                      no-radius
                      @update:model-value="($event) => {
                        inputs['paymentMethod'].isCard = props.isPaymentCard($event);
                        setPaymentValue('paymentMethod', $event);
                      }"
                      v-slot="{ option, isSelected }"
          >
            <div class="flex items-center"
                 style="padding-top: 0.5rem; padding-bottom: 0.5rem; width: 100%; gap: 1rem"
            >
              <template v-if="option.icon">

                <font-awesome-icon class="me-2"
                                   :icon="option.icon"
                                   :style="[isSelected ? {background: `#${option['icon_color']}`} : {color: `#${option['icon_color']}`}]"
                                   size="lg"
                />

              </template>

              <span>{{ option.label }}</span>

            </div>

          </maz-select>

        </div>
      </div>
    </li>

  </ul>

  <template v-if="inputs['paymentMethod'].isCard" >

    <transition name="nested" mode="out-in">

      <div>

        <!--Card Payment Form-->
        <card-payment-form :generate-random-card-number="true"
                           @card-name="cardName = $event"
                           @card-number="cardNumber = $event"
                           @card-expiry="cardExpiry = $event"
                           @card-security-code="cardSecurityCode = $event"
                           @is-valid="isValidPaymentForm = $event"
                           @is-required-set="isPaymentFormSet = $event"
        />

        <div class="row mt-2 mb-0 pb-0 pt-2">
          <div class="title" style="margin: 0!important;">
            <div class="row justify-content-between">
              <div class="col-md-12">
                <h5>
                  <b>Billing address</b>
                </h5>
              </div>
            </div>
          </div>
        </div>

        <ul class="payment-info-details" style="margin-bottom: 0!important;">

          <li>
            <div class="row row-cols-auto ms-0 me-0 clearfix">

              <div class="col-md-6 mb-3 ps-0 pe-1">

                <label for="use-shipping-address" class="form-check-label">
                  <input type="checkbox"
                         class="form-check-input"
                         id="use-shipping-address"
                         name="use-shipping-address"
                         v-model="info['useShippingAddress']"
                         :value="info['useShippingAddress']"
                         @change="($event) => {
                           setPaymentValue('useShippingAddress', $event.target.checked);
                           $event.target.checked ? '' : getCountries();
                           checkValidation();
                         }"
                  />
                  <span>Same as shipping address</span>
                </label>

              </div>
            </div>
          </li>

        </ul>

        <template v-if="!dataLoading">

          <maz-details-info-form v-if="info['useShippingAddress'] === false"
                                 :details="props.paymentDetails"
                                 :set-details-method="props.setPaymentDetails"
                                 :countries="countries"
                                 :is-billing-address="true"
                                 :auto-focus="false"
                                 @is-valid="($event) => {
                                   isValidBillingAddressForm = $event
                                 }"
                                 @is-required-set="($event) => {
                                   isBillingAddressFormSet = $event
                                 }"
          />

        </template>

        <content-loader-component v-else style="transition: all 0.3s ease-in-out" />

      </div>

    </transition>

  </template>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import CardPaymentForm from "@/components/CardPaymentForm";
import MazDetailsInfoForm from "@/components/MazDetailsInfoForm";
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import {axios} from "@/common/api.axios";
import { ref, defineProps, defineEmits, watch, onMounted, onBeforeMount } from "vue";

export default {
  name: "MazPaymentInfoForm",
  components: {
    CardPaymentForm,
    MazDetailsInfoForm,
    ContentLoaderComponent
  }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/

const props = defineProps({
  paymentDetails: {
    type: Object,
    // Object or array defaults must be returned from a factory function.
    // The function receives the raw props received by the component as the argument.
    default(rawProps) {
      return {}
    }
  },
  paymentMethods: {
    type: Array,
    required: true
  },
  setPaymentDetails: {
    type: Function,
    required: true
  },
  isPaymentCard: {
    type: Function,
    required: true
  },
  countriesEndpoint: {
    type: String,
    required: true
  }
});
const info = ref(props.paymentDetails);
const inputs = ref({});
const countries = ref([{label: '', value: ''}]);
const dataLoading = ref(false);
const isValidPaymentForm = ref(false);
const isPaymentFormSet = ref(false);
const isValidBillingAddressForm = ref(false);
const isBillingAddressFormSet = ref(false);
const cardName = ref(null);
const cardNumber =  ref(null);
const cardExpiry = ref(null);
const cardSecurityCode = ref(null);
// Define the list of events that you want to emit.
const emits = defineEmits(
    [
      'isValid',
      'isRequiredSet',
      'cardName',
      'cardNumber',
      'cardExpiry',
      'cardSecurityCode'
    ]
);

// Define functions
const setPaymentValue = async (key, val) =>{
  /**
   * Method to set payment info key: value
   */

  if(inputs.value[key].isValid === false){
    return false
  }

  // In case everything is ok, set payment info value in the store.
  // Note: Since we store boolean values, so be careful when change 'val' to string because
  //       it will not work in comparison or with if statements.
  await props.setPaymentDetails(key, val);
};
const getCountries = async () => {
  /**
   * Method to retrieve countries list from backend server
   */

  dataLoading.value = true;

  try {
    let response = await axios.get(props.countriesEndpoint);
    countries.value = response.data
  }
  catch (error) {
    console.log("Error while trying to retrieve the requested data from backend server!");
  }
  finally {
    dataLoading.value = false;
  }
};
const isValidPayment = () => {
  /**
   * Return true if payment form inputs is set correctly and all required inputs are set,
   * otherwise return false.
   */

  if (isPaymentFormSet.value === false) {
    // Emits a false value for 'isRequiredSet' event.
    emits('isRequiredSet', false);
    // No need to continue the loop.
    return
  }

  if (isValidPaymentForm.value === false) {
    // Emits a false value for 'isValid' event.
    emits('isValid', false);
    // No need to continue the loop.
    return
  }

  // In case everything pass ok, return true value.
  return true;
};
const isValidBillingAddress = () => {
  /**
   * Return true if billing address form inputs is set correctly and all required inputs are set,
   * otherwise return false.
   */

  if (isBillingAddressFormSet.value === false) {
    // Emits a false value for 'isRequiredSet' event.
    emits('isRequiredSet', false);
    // No need to continue the loop.
    return
  }

  if (isValidBillingAddressForm.value === false) {
    // Emits a false value for 'isValid' event.
    emits('isValid', false);
    // No need to continue the loop.
    return
  }

  // In case everything pass ok, return true value.
  return true;
};
const checkValidation = () => {
  /**
   * Method to check validation of required inputs/forms
   */

  // Check form inputs.
  for (let key of Object.keys(inputs.value)){
    if(inputs.value[key].isRequired === true && info.value[key] === ''){
      // Emits a false value for 'isRequiredSet' event.
      emits('isRequiredSet', false);
      // No need to continue the loop.
      return
    }
    else if(inputs.value[key].isValid === false){
      // Emits a false value for 'isValid' event.
      emits('isValid', false);
      // No need to continue the loop.
      return
    }
  }

  // If everything is ok, then check forms.

  // Check if selected payment method is card or not.
  if (inputs.value['paymentMethod'].isCard === true) {

    let validPayment = isValidPayment();

    // Initialize variable for billing address validation.
    let validBillingAddress = false;

    // Check if 'useShippingAddress' checkbox input is false.
    if (info.value['useShippingAddress'] === false) {

      // if so, check billing address form.
      validBillingAddress = isValidBillingAddress();

      if (validPayment === true && validBillingAddress === true) {
        emits('isRequiredSet', true);
        emits('isValid', true);
      }
    }
    else {
      // in case 'useShippingAddress' is set to true, then we only need to check payment form.
      if (validPayment === true) {
        emits('isRequiredSet', true);
        emits('isValid', true);
      }
    }

    // Emit payment card details.
    emits('cardName', cardName.value);
    emits('cardNumber', cardNumber.value);
    emits('cardExpiry', cardExpiry.value);
    emits('cardSecurityCode', cardSecurityCode.value);

  }
  else{
    // in case selected payment method is not card.
    emits('isRequiredSet', true);
    emits('isValid', true);
  }
};

// life-cycles

// Note: we can't access methods at initialize time because these methods could be not initialized yet.
onBeforeMount(() => {

  /*
    Note: Here we have checkbox input, so we need either true or false value and since we could
          get 'undefined' value, so we need to set a value:

         info.value['useShippingAddress'] === false ? info.value['useShippingAddress'] : true
   */

  // In case it's not set, then set the value to be true.
  if (info.value['useShippingAddress'] === undefined){
    info.value['useShippingAddress'] = true;
  }
  else if(info.value['useShippingAddress'] === false){
    // Get countries array from backend
    getCountries();
  }

  inputs.value = {
    paymentMethod: {
      isValid: true,
      isRequired: true,
      isCard: props.isPaymentCard(info.value['paymentMethod']),
      options: props.paymentMethods
    },
    useShippingAddress: {
      isValid: true,
      isRequired: true
    },
  };
});

onMounted(() => {

  // Trigger checkValidation() method
  checkValidation();

  let requiredInputs = [isPaymentFormSet, isBillingAddressFormSet];
  let validInputs = [isValidPaymentForm, isValidBillingAddressForm];

  // Watch
  // Note: if you are watching single object/array then no need to use getter way to watch reactive values.
  watch(
      [() => requiredInputs, () => validInputs, () => inputs.value],
      (
          [currentRequiredInputs, currentValidInputs, currentInputs],
          [prevRequiredInputs, prevValidInputs, prevInputs]
      ) => {
        checkValidation();
      },
      {
        deep: true
      }
  );

});

</script>

<style lang="scss">

$main-color: #0F1111;

.payment-info-details{
  list-style: none;
  padding-top: 8px;
  padding-left: 0;
}

hr{
    margin-top: 2rem;
}

label{
  font-weight: 400;
  color: $main-color;
}

label, option {
  font-size: 14px;
}
input::placeholder {
  font-size: 13px;
}

.form-check-label span:hover {
  transition: color 200ms ease-in-out;
  color: rgb(204, 12, 57) !important;
}

.form-check-input {
  margin-right: 5px;
}

// for phones and tablets
@media(max-width:767px){
  .related-field{
    padding-left: 0!important;
  }
  input::placeholder {
    font-size: 12px;
  }
}
// for big screens
@media(min-width:768px) {
  .related-field {
    padding-left: 10px !important;
  }
}

// Override the black color of Maz input
:root {
  --maz-color-black: hsl(180, 6%, 6%)!important;
  --maz-color-black-contrast: hsl(0deg 0% 100%);
}

.--bottom{
  max-width: 240px!important;
  max-height: 250px!important;
}

</style>