<template>

  <div class="row row-cols-auto mb-3">

    <div class="col-md-6" style="min-width: 230px;">

      <div :class="['container', preload ? 'preload' : '']">
        <div ref="creditcard"
             :class="['creditcard', flip ? 'flipped' : '']"
             @click="flip = !flip"
        >
          <div class="front">

            <div ref="ccSingle" id="cc-single" v-html="ccSingleInner">

            </div>

            <svg version="1.1" id="card-front"
                 xmlns="http://www.w3.org/2000/svg"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 x="0px" y="0px" viewBox="0 0 750 471"
                 style="enable-background:new 0 0 750 471;"
                 xml:space="preserve">

                    <g id="Front">
                        <g id="CardBackground">
                            <g id="Page-1_1_">
                                <g id="amex_1_">
                                    <path id="Rectangle-1_1_"
                                          :class="['light-color', baseLightColor]"
                                          d="M40,0h670c22.1,0,40,17.9,40,40v391c0,22.1-17.9,40-40,40H40c-22.1,0-40-17.9-40-40V40C0,17.9,17.9,0,40,0z"/>
                                </g>
                            </g>
                          <path :class="['dark-color', baseDarkColor]"
                                d="M750,431V193.2c-217.6-57.5-556.4-13.5-750,24.9V431c0,22.1,17.9,40,40,40h670C732.1,471,750,453.1,750,431z"/>
                        </g>

                      <text ref="svgNumber" transform="matrix(1 0 0 1 60.106 295.0121)" id="svg-number" class="st2 st3 st4">
                        {{cardDefaultValues.cardNumber}}
                      </text>

                      <text ref="svgName" transform="matrix(1 0 0 1 54.1064 428.1723)" id="svg-name" class="st2 st5 st6">
                        {{cardDefaultValues.cardholderName}}
                      </text>

                      <text transform="matrix(1 0 0 1 54.1074 389.8793)" class="st7 st5 st8">cardholder name</text>
                      <text transform="matrix(1 0 0 1 479.7754 388.8793)" class="st7 st5 st8">expiration</text>
                      <text transform="matrix(1 0 0 1 65.1054 241.5)" class="st7 st5 st8">card number</text>

                      <g>

                        <text ref="svgExpire" transform="matrix(1 0 0 1 574.4219 433.8095)" id="svg-expire" class="st2 st5 st9">
                          {{cardDefaultValues.cardExpire}}
                        </text>
                        <text transform="matrix(1 0 0 1 479.3848 417.0097)" class="st2 st10 st11">VALID</text>
                        <text transform="matrix(1 0 0 1 479.3848 435.6762)" class="st2 st10 st11">THRU</text>
                        <polygon class="st2" points="554.5,421 540.4,414.2 540.4,427.9"/>
                      </g>

                      <g id="cchip">
                        <g>
                          <path class="st2" d="M168.1,143.6H82.9c-10.2,0-18.5-8.3-18.5-18.5V74.9c0-10.2,8.3-18.5,18.5-18.5h85.3c10.2,0,18.5,8.3,18.5,18.5v50.2C186.6,135.3,178.3,143.6,168.1,143.6z"/>
                        </g>
                        <g>
                          <g>
                            <rect x="82" y="70" class="st12" width="1.5" height="60"/>
                          </g>
                          <g>
                            <rect x="167.4" y="70" class="st12" width="1.5" height="60"/>
                          </g>
                          <g>
                            <path class="st12" d="M125.5,130.8c-10.2,0-18.5-8.3-18.5-18.5c0-4.6,1.7-8.9,4.7-12.3c-3-3.4-4.7-7.7-4.7-12.3
                            c0-10.2,8.3-18.5,18.5-18.5s18.5,8.3,18.5,18.5c0,4.6-1.7,8.9-4.7,12.3c3,3.4,4.7,7.7,4.7,12.3
                            C143.9,122.5,135.7,130.8,125.5,130.8z M125.5,70.8c-9.3,0-16.9,7.6-16.9,16.9c0,4.4,1.7,8.6,4.8,11.8l0.5,0.5l-0.5,0.5
                            c-3.1,3.2-4.8,7.4-4.8,11.8c0,9.3,7.6,16.9,16.9,16.9s16.9-7.6,16.9-16.9c0-4.4-1.7-8.6-4.8-11.8l-0.5-0.5l0.5-0.5
                            c3.1-3.2,4.8-7.4,4.8-11.8C142.4,78.4,134.8,70.8,125.5,70.8z"
                            />
                          </g>
                          <g>
                            <rect x="82.8" y="82.1" class="st12" width="25.8" height="1.5"/>
                          </g>
                          <g>
                            <rect x="82.8" y="117.9" class="st12" width="26.1" height="1.5"/>
                          </g>
                          <g>
                            <rect x="142.4" y="82.1" class="st12" width="25.8" height="1.5"/>
                          </g>
                          <g>
                            <rect x="142" y="117.9" class="st12" width="26.2" height="1.5"/>
                          </g>
                        </g>
                      </g>
                    </g>

              <g id="Back"></g>
            </svg>
          </div>

          <div class="back">
            <svg version="1.1" id="card-back" xmlns="http://www.w3.org/2000/svg"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 x="0px" y="0px" viewBox="0 0 750 471"
                 style="enable-background:new 0 0 750 471;"
                 xml:space="preserve"
            >
              <g id="Front">
                <line class="st0" x1="35.3" y1="10.4" x2="36.7" y2="11"/>
              </g>

              <g id="Back">

                <g id="Page-1_2_">
                  <g id="amex_2_">
                    <path id="Rectangle-1_2_" :class="['dark-color', baseDarkColor]" d="M40,0h670c22.1,0,40,17.9,40,40v391c0,22.1-17.9,40-40,40H40c-22.1,0-40-17.9-40-40V40C0,17.9,17.9,0,40,0z"/>
                  </g>
                </g>
                <rect y="61.6" class="st2" width="750" height="78"/>
                <g>
                  <path class="st3" d="M701.1,249.1H48.9c-3.3,0-6-2.7-6-6v-52.5c0-3.3,2.7-6,6-6h652.1c3.3,0,6,2.7,6,6v52.5C707.1,246.4,704.4,249.1,701.1,249.1z"/>
                  <rect x="42.9" y="198.6" class="st4" width="664.1" height="10.5"/>
                  <rect x="42.9" y="224.5" class="st4" width="664.1" height="10.5"/>
                  <path class="st5" d="M701.1,184.6H618h-8h-10v64.5h10h8h83.1c3.3,0,6-2.7,6-6v-52.5C707.1,187.3,704.4,184.6,701.1,184.6z"/>
                </g>

                <text transform="matrix(1 0 0 1 621.999 227.2734)" ref="svgSecurity" id="svg-security" class="st6 st7">
                  {{cardDefaultValues.cardSecurityCode}}
                </text>

                <g class="st8">
                  <text transform="matrix(1 0 0 1 518.083 280.0879)" class="st9 st6 st10">security code</text>
                </g>
                <rect x="58.1" y="378.6" class="st11" width="375.5" height="13.5"/>
                <rect x="58.1" y="405.6" class="st11" width="421.7" height="13.5"/>

                <text transform="matrix(1 0 0 1 59.5073 228.6099)" ref="svgNameBack" id="svg-name-back" class="st12 st13">
                  {{cardDefaultValues.cardholderName}}
                </text>

              </g>

            </svg>
          </div>
        </div>
      </div>
    </div >

    <div class="col-md-6" style="min-width: 230px;">
      <div class="form-container">

        <ul class="payment-info-details">

          <li>

            <div id="first-li" class="row row-cols-auto ms-0 me-0 pt-0 mt-3 clearfix">

              <div class="col-md-12 pt-0 mt-0 pe-1 ps-0">

                <div class="input-wrapper">
                  <label for="name">Name*</label>
                  <input :ref="cardName.el"
                         v-imask="cardName.mask"
                         type="text"
                         id="name"
                         :class="[cardNameValid ? 'valid' : '']"
                         autocomplete="off"
                         :required="cardName.isRequired"
                         @focus="($event) => {
                           flip = false;
                           dynamicInputLabel($event);
                         }"
                         @blur="dynamicInputLabel($event, true)"
                         @accept="($event) => {
                           setSvgInnerHTML(
                               $event.target.value,
                               cardDefaultValues.cardholderName,
                               [svgName, svgNameBack]
                           );
                           cardNameValid = false;
                           // Also if current input value is empty, trigger isValidForm()
                           $event.target.value === '' ? isValidForm() : '';
                         }"
                         @complete="($event) => {
                           $event.target.value !== '' ? cardNameValid = true : '';
                         }"
                  />
                </div>
              </div>

            </div>

          </li>

          <li>

            <div :class="['row row-cols-auto ms-0 me-0 pt-0 clearfix', props.generateRandomCardNumber ? 'mt-4' : 'mt-2']">

              <div class="col-md-12 pt-0 mt-0 pe-1 ps-0">

                <div class="input-wrapper" id="card-number-wrapper">

                  <span v-if="props.generateRandomCardNumber"
                        id="generate-card"
                        @click="randomCard">Generate random</span>

                  <label for="card-number">Card Number*</label>
                  <input :ref="cardNumber.el"
                         v-imask="cardNumber.mask"
                         type="text"
                         id="card-number"
                         :class="[cardNumberValid ? 'valid' : '']"
                         inputmode="numeric"
                         pattern="[0-9]*"
                         autocomplete="off"
                         :required="cardNumber.isRequired"
                         @focus="($event) => {
                           flip = false;
                           dynamicInputLabel($event);
                         }"
                         @blur="dynamicInputLabel($event, true)"
                         @accept="($event) => {
                           setSvgInnerHTML($event.target.value, cardDefaultValues.cardNumber,[svgNumber]);
                           ($event.target.value).length <= 0 ? selectCardType($event) : '';
                           cardNumberValid = false;
                           // Also if current input value is empty, trigger isValidForm()
                           $event.target.value === '' ? isValidForm() : '';
                         }"
                         @complete="($event) => {
                           selectCardType($event);
                           $event.target.value !== '' ? cardNumberValid = true : '';
                         }"
                  />

                  <svg ref="ccIcon" v-html="ccIconInner" id="cc-icon"
                       class="cc-icon" width="750" height="471"
                       viewBox="0 0 750 471" version="1.1"
                       xmlns="http://www.w3.org/2000/svg"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                  >
                  </svg>
                </div>

              </div>

            </div>

          </li>

          <li>

            <div class="row row-cols-auto ms-0 me-0 pt-0 mt-2 clearfix">

              <div class="col-md-6 pt-0 mt-0 pe-1 ps-0 mb-2" style="min-width: 160px;">

                <div class="input-wrapper">
                  <label for="expiration-date">Expire (mm/yy)*</label>
                  <input :ref="cardExpireDate.el"
                         v-imask="cardExpireDate.mask"
                         id="expiration-date"
                         :class="[cardExpireDateValid ? 'valid' : '']"
                         type="text"
                         pattern="[0-9]*"
                         inputmode="numeric"
                         autocomplete="off"
                         :required="cardExpireDate.isRequired"
                         @focus="($event) => {
                           flip = false;
                           dynamicInputLabel($event);
                         }"
                         @blur="dynamicInputLabel($event, true)"
                         @accept="($event) => {
                           setSvgInnerHTML(
                               $event.target.value,
                               cardDefaultValues.cardExpire,
                               [svgExpire]
                           );
                           cardExpireDateValid = false;
                           // Also if current input value is empty, trigger isValidForm()
                           $event.target.value === '' ? isValidForm() : '';
                         }"
                         @complete="$event.target.value !== '' ? cardExpireDateValid = true : ''"
                  />
                </div>

              </div>

              <div class="col-md-6 ps-0 pt-0 mt-0 pe-1 related-field" style="min-width: 160px;">

                <div class="input-wrapper">
                  <font-awesome-icon id="eye-icon"
                                     :icon="['fa-solid', showCode ? 'fa-eye-slash' : 'fa-eye']"
                                     @click="() => {
                                       flip = true;
                                       updateCardSecurityCodeMask();
                                     }"
                  />
                  <label for="security-code">CCV*</label>
                  <input :ref="cardSecurityCode.el"
                         v-imask="cardSecurityCode.mask"
                         id="security-code"
                         :class="[cardSecurityCodeValid ? 'valid' : '']"
                         type="text"
                         pattern="[0-9]*"
                         autocomplete="off"
                         :required="cardSecurityCode.isRequired"
                         @focus="($event) => {
                           flip = true;
                           dynamicInputLabel($event);
                         }"
                         @blur="($event) => {
                           // flip = false
                           dynamicInputLabel($event, true)
                         }"
                         @accept="($event) => {
                           setSvgInnerHTML(
                               $event.target.value,
                               cardDefaultValues.cardSecurityCode,
                               [svgSecurity]
                           );
                           cardSecurityCodeValid = false;
                           // Also if current input value is empty, trigger isValidForm()
                           $event.target.value === '' ? isValidForm() : '';
                         }"
                         @complete="$event.target.value !== '' ? cardSecurityCodeValid = true : ''"
                  />

                </div>

              </div>

            </div>

          </li>

        </ul>

<!--        <div class="field-container">-->
<!--          <label for="security-code">Security code</label>-->

<!--          <input ref="cardSecurityCode"-->
<!--                 id="security-code"-->
<!--                 type="text"-->
<!--                 pattern="[0-9]*"-->
<!--                 inputmode="numeric"-->
<!--                 autocomplete="off"-->
<!--                 @focus="flip = true"-->
<!--                 @input="setSvgInnerHTML(-->
<!--                     '*'.repeat(($event.target.value).length),-->
<!--                     $event.data,-->
<!--                     cardDefaultValues.cardSecurityCode,-->
<!--                     [svgSecurity],-->
<!--                     /^(?=.{1,4}$)(?!\s)[*]+$/,-->
<!--                     4-->
<!--                 )"-->
<!--          >-->

<!--        </div>-->

      </div>
    </div>

  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/

/*
  Note: about vue-mask:
        1- using directive v-imask it's working with defined mask:

           const cardNameMask = { mask: /(?=^.{0,50}$)(^[A-Za-z]*$)/, dispatch: () => {}  };

           Then you can use it:

           <input v-imask="cardNameMask" @accept="<method>" @complete="method" />

           OR direct type mask:

           <input v-imask="Number" />

        2- using the 'mask' object that return from useIMask() method will not work due it's not initialize
           yet at setup time of component.
        3- 'el' (represent InputMask class) and 'mask' object of useIMask() method are reactive and should
           use 'value' property to access its properties, 'el' can be use as ref for HTML input or use 'mask'
           with 'v-imask' directive and add null ref to that input to access 'maskRef' details.

           <input ref="el" @input="method()">

        4- the HTML input that use 'el' object (initialized by useIMask()) as ref can't use event @accept and @complete.
        5- any event triggered by InputMask contains 'detail' object that can be used to access to that class
           details.
        6- 'maskRef' object represent 'mask' and anything execute/changed by it will update UI too, while
           'maskRef.masked' have same options but will not update the UI.
        7- you can access 'maskRef' through InputMask:

           $event.detail.el.input.maskRef
           <ref-to>.el.value.maskRef

        8- if you tried to change value of InputMask (HTML input element) in direct way will face an error
           tells you have to use 'mask.updateValue()' where mask means => maskRef object.
        9- if you want to update your mask options that being use by v-imask you SHOULD NOT delete any
           property because any change will not update 'displayValue' of 'masked' object.
        10- to force update your InputMask you can use:

            <ref-to>.el.value.maskRef.updateControl()

        11- to force to update 'el.value.value' from 'displayValue':

            <ref-to>.el.value.maskRef_onChange()

        12- to force fire of all events that related to InputMask and that satisfy the condition of trigger:

            <ref-to>.el.value.maskRef._fireChangeEvents()

        13- if you want to trigger specific @accept or @complete directly whether it satisfy the condition
            of trigger or not:

            <ref-to>.el.value.maskRef._listeners.accept[0]()
            <ref-to>.el.value.maskRef._listeners.complete[0]()

        14- to update your mask options at running time:

            <ref-to>.el.value.maskRef.updateOptions(<updated-mask-object>);

        15- The order of event trigger of InputMask is:
            @accept as first
            @complete as second

        16- To access mask/regex of InputMask:

            A- for object that use multiple masks with dispatch method:

               <ref-to>.el.value.maskRef.masked.currentMask

            B- for object that use single mask:

               <ref-to>.el.value.maskRef.mask
 */

import {
  cardNameProps, cardExpireDateProps, cardNumberProps, cardSecurityCodeProps,
  cardSecurityNoSecretCodeProps
} from "@/common/inputMask"
// import {cardPaymentMask} from "@/common/inputMask";
// import { IMaskComponent } from 'vue-imask';
import * as paymentSVGIcon from "@/assets/javascript/paymentCardIcons";
import {dynamicInputLabel} from "@/assets/javascript/dynamicInputLabel";
import { defineProps, ref, onMounted, watch, defineEmits } from "vue";

export default {
  name: "CardPaymentForm",
  // components:{
  //   imaskInput: IMaskComponent
  // }
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  generateRandomCardNumber: {
    type: Boolean,
    default: true
  }
});

let date = new Date();
let nextYear = (date.getFullYear() % 100) + 1;
let currentMonth = date.getMonth() + 1;

if (currentMonth < 10){
  currentMonth = `0${currentMonth}`;
}
const cardDefaultValues = {
  cardholderName: 'John Doe',
  cardNumber: '0123 4567 8910 1112',
  cardExpire: `${currentMonth}/${nextYear}`,
  cardSecurityCode: '987'
};
const preload = ref(true);
const flip = ref(false);
const creditcard = ref(null);
const svgName = ref(null);
const svgNameBack = ref(null);
const svgNumber = ref(null);
const svgExpire = ref(null);
const svgSecurity = ref(null);
const ccIcon = ref(null);
const ccSingle = ref(null);
const baseLightColor = ref('grey');
const baseDarkColor = ref('grey-dark');
const ccIconInner = ref(null);
const ccSingleInner = ref(null);
const showCode = ref(false);

// First method
// const {el: cardName, mask: cardNameMask} = cardPaymentMask('cardName');

// Second method
// const cardNameVMask = {mask: /^(?=.{0,20}$)(?!\s)((?:[A-Za-z]+\s?){1,3}$)/};

// Third method
const cardName = {
  el: ref(null),
  mask: cardNameProps,
  isRequired: true,
};
const cardNumber = {
  el: ref(null),
  mask: cardNumberProps,
  isRequired: true,
};
const cardExpireDate = {
  el: ref(null),
  mask: cardExpireDateProps,
  isRequired: true,
};
const cardSecurityCode = {
  el: ref(null),
  mask: cardSecurityCodeProps,
  isRequired: true,
};

const cardNameValid = ref(false);
const cardNumberValid = ref(false);
const cardExpireDateValid = ref(false);
const cardSecurityCodeValid = ref(false);
let validInputs = [cardNameValid, cardNumberValid, cardExpireDateValid, cardSecurityCodeValid];

const testCards = [
    '4000056655665556',
    '5200828282828210',
    '371449635398431',
    '6011000990139424',
    '30569309025904',
    '3566002020360505',
    '6200000000000005',
    '6759649826438453',
];

// Define the list of events that you want to emit.
const emits = defineEmits(['isValid', 'isRequiredSet']);

// Define functions
const setSvgInnerHTML = (val, defaultVal, elements) => {
  /**
   * Method to set innerHTML of card fields
   *
   * @param {String} val Represent the input field value of triggered event.
   * @param {String} defaultVal Represent the default value to set in input field for
   * provided array element in case the provided 'val' length is zero.
   * @param {Array} elements Represent the array of elements to change their inner HTML.
   */

  // Get the length of 'val'.
  let len = val.length;

  if (len === 0) {
    for (let ele of elements) {
      ele.innerHTML = defaultVal;
      // ele.innerText = defaultVal;
    }
  }
  else {
    for (let ele of elements) {
      ele.innerHTML = val;
      // ele.innerText = val;
    }
  }
};
const swapColor = (baseColor) => {
  /**
   * color swap method
   */

  // Change base color
  baseLightColor.value = baseColor;
  baseDarkColor.value = `${baseColor}-dark`;

  // This is the regular way to do it in javascript.
  // document.querySelectorAll('.light-color').forEach( (input) => {
  //   input.setAttribute('class', '');
  //   input.setAttribute('class', 'light-color ' + baseColor);
  // });
  // document.querySelectorAll('.dark-color').forEach( (input) => {
  //   input.setAttribute('class', '');
  //   input.setAttribute('class', 'dark-color ' + baseColor + '-dark');
  // });
};
const selectCardType = (e) => {
  /**
   * Select card type depending on current card number
   */

  // From the custom imask event detail, get card type from current selected mask.
  let cardType = e.detail.masked.currentMask.cardType;

  switch (cardType) {
    case 'american express':
      //ccIcon.value.innerHTML = paymentSVGIcon.amex;
      //ccSingle.value.innerHTML = paymentSVGIcon.amexSingle;
      ccIconInner.value = paymentSVGIcon.amex;
      ccSingleInner.value = paymentSVGIcon.amexSingle;
      swapColor('green');
      break;
    case 'visa':
      ccIconInner.value = paymentSVGIcon.visa;
      ccSingleInner.value = paymentSVGIcon.visaSingle;
      swapColor('lime');
      break;
    case 'diners':
      ccIconInner.value = paymentSVGIcon.diners;
      ccSingleInner.value = paymentSVGIcon.dinersSingle;
      swapColor('orange');
      break;
    case 'discover':
      ccIconInner.value = paymentSVGIcon.discover;
      ccSingleInner.value = paymentSVGIcon.discoverSingle;
      swapColor('purple');
      break;
    case ('jcb' || 'jcb15'):
      ccIconInner.value = paymentSVGIcon.jcb;
      ccSingleInner.value = paymentSVGIcon.jcbSingle;
      swapColor('red');
      break;
    case 'maestro':
      ccIconInner.value = paymentSVGIcon.maestro;
      ccSingleInner.value = paymentSVGIcon.maestroSingle;
      swapColor('yellow');
      break;
    case 'mastercard':
      ccIconInner.value = paymentSVGIcon.mastercard;
      ccSingleInner.value = paymentSVGIcon.mastercardSingle;
      swapColor('lightblue');
      break;
    case 'union pay':
      ccIconInner.value = paymentSVGIcon.unionPay;
      ccSingleInner.value = paymentSVGIcon.unionPaySingle;
      swapColor('cyan');
      break;
    default:
      ccIconInner.value = '';
      ccSingleInner.value = '';
      swapColor('grey');
      break;
  }
};
const updateCardSecurityCodeMask = () => {
  /**
   * Change InputMask mask options of security code input (CCV).
   */

  // Get the value of security code input
  // Note: this variable is read only.
  // let val = document.getElementById("security-code").value;
  // let val = cardSecurityCode.el.value.maskRef.unmaskedValue;

  // Since our card CCV input using array of mask, then we need to get current mask.
  let currentMask = cardSecurityCode.el.value.maskRef.masked.currentMask;

  // Check if 'displayChar' property in the mask is exists and has no empty value, then update
  // the mask to one that has no secret display of text.
  if (!['', undefined].includes(currentMask.displayChar)) {
    cardSecurityCode.mask = cardSecurityNoSecretCodeProps;
    showCode.value = true;
  }
  else {
    // Otherwise set the mask with properties that allow secret text display.
    cardSecurityCode.mask = cardSecurityCodeProps;
    showCode.value = false;

    // If you want to change value directly, will cause warning to use 'mask.updateValue()'.
    // document.getElementById("security-code").value = '*'.repeat(val.length);
    // cardSecurityCode.el.value.maskRef.el.value = '*'.repeat(val.length);
  }

  // Update mask options of InputMask.
  cardSecurityCode.el.value.maskRef.updateOptions(cardSecurityCode.mask);

  // Actually we want to trigger all events that are satisfy the conditions to trigger (means
  // @accept and @complete).
  cardSecurityCode.el.value.maskRef._fireChangeEvents();
};
const randomCard = () => {
  /**
   * Generate random card number from list of known test numbers
   */

  // Generate random number.
  let randomNumber = Math.floor(Math.random() * testCards.length);

  // Trigger focus event of 'card-number' HTML element.
  // Note: you can do it using ref if that element has or by using document DOM.

  // let ele = document.getElementById("card-number");
  let ele = cardNumber.el.value;

  // Check for current focus element in DOM is the same as required element then no need to re-focus.
  // Note: this line of code will always find the current focus element is not card number input due
  //       we clicked on 'generate random' <span>
  document.activeElement !== ele ? ele.focus() : '';

  // Set the random number into card number input.
  // document.getElementById("card-number").value = testCards[randomNumber];
  cardNumber.el.value.maskRef.value = testCards[randomNumber];
};
const isValidForm = () => {
  /**
   * Return true if form inputs is set correctly and all required inputs are set, otherwise return false.
   */

  let eleArray = [cardName.el, cardNumber.el, cardExpireDate.el, cardSecurityCode.el]

  for (let el of eleArray){
    // Check if 'el' has required attribute and its current field value is empty.
    if(el.value.attributes.required && el.value.value === ''){
      // Emits a false value for 'isRequiredSet' event.
      emits('isRequiredSet', false);
      // No need to continue the loop.
      return
    }
  }
  for (let item of validInputs){
    // Check if item value is false.
    if (item.value === false) {
      // Emits a false value for 'isValid' event.
      emits('isValid', false);
      // No need to continue the loop.
      return
    }
  }

  // In case everything pass ok, emits the required events with true value.
  emits('isRequiredSet', true);
  emits('isValid', true);
};

// const setSvgInnerHTML = (val, data, defaultVal, elements, regex=/[\s\S]*/, maxChars=0) => {
//   /**
//    * Method to set innerHTML of card fields
//    *
//    * @param {String} val Represent the input field value of triggered event.
//    * @param {String} data Represent the current entered string in the input field.
//    * @param {String} defaultVal Represent the default value to set in input field for
//    * provided array element in case the provided 'val' length is zero.
//    * @param {Array} elements Represent the array of elements to change their inner HTML.
//    * @param {String} regex Optional, represent the regex for test the provided 'val', default match everything.
//    * @param {Number} maxChars Optional, represent the maximum length of characters that the provided 'val'
//    * should not exceed, default is zero and means infinity.
//    */
//
//   /*
//     Note: Maybe wondering why we don't use for example:
//
//           cardNameMask.value.unmaskedValue
//
//           OR:
//
//           cardNameMask.value.value
//
//           OR:
//
//           cardNameMask.value.maskedValue
//
//           This due that masked value return the previous field value not the current one.
//    */
//   /*
//     Info: To get the whole input field value of cardName element for example:
//
//           let val = cardNameMask.value.el.value;
//
//           is the same process of:
//
//           let val = cardName.value.value;
//    */
//
//   // Test the inserted current input field string using mask regex.
//   // Note: we use RegExp() method in case the provided regex is text (between two quotes)
//   let valid = RegExp(regex).test(val);
//   // Get the length of 'val'.
//   let len = val.length;
//
//   /*
//     Important: in our mask regex, the space (empty string) consider as valid value
//                but its length zero if only emtpy string set in the input field, so
//                this is why we put (val.length === 0) as first condition.
//    */
//   if (len === 0) {
//     for (let ele of elements) {
//       ele.innerHTML = defaultVal;
//     }
//   }
//   else if(valid && ( maxChars === 0 || len <= Number(maxChars))) {
//     for (let ele of elements) {
//       ele.innerHTML = val;
//     }
//   }
// };

// Life cycles
onMounted(() => {

  // CREDIT CARD IMAGE JS
  // document.querySelector('.preload').classList.remove('preload');
  preload.value = false;

  // Trigger 'isValidForm' method the moment template is mounted.
  isValidForm();

  // Watch the 'validInputs' array of boolean items.
  watch(validInputs, (currentValue, oldValue) =>
      {
        isValidForm();
      },
      {
        //deep: true,
        //lazy: true
      }
  );
});

</script>

<style lang="scss" scoped>

/////////////////////////////
// Payment Card style
////////////////////////////

$main-color: #0F1111;

//.form-container .field-container:first-of-type {
//  grid-area: name;
//}
//
//.form-container .field-container:nth-of-type(2) {
//  grid-area: number;
//}
//
//.form-container .field-container:nth-of-type(3) {
//  grid-area: expiration;
//
//}

//.form-container .field-container:nth-of-type(4) {
//  grid-area: security;
//}

//.form-container {
//  display: grid;
//  grid-column-gap: 10px;
//  grid-template-columns: auto auto;
//  grid-template-rows: 90px 90px 90px;
//  grid-template-areas: "name name""number number""expiration security";
//  max-width: 400px;
//  padding: 20px;
//  color: #707070;
//}

//.field-container input {
//  -webkit-box-sizing: border-box;
//  box-sizing: border-box;
//}

//.field-container {
//  position: relative;
//}

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}

.payment-title {
  width: 100%;
  text-align: center;
}

.payment-info-details{
  list-style: none;
  padding: 0;
}

label {
  width: -moz-max-content;
  width: max-content;
  display: -webkit-box;
  display: -ms-flexbox;
  -webkit-box-align: center;
  -ms-flex-align: center;
  -webkit-box-pack: center;

  pointer-events: none;
  display: block;
  align-items: center;
  justify-content: center;
  webkit-transform-origin: top left;
  transform-origin: top left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  left: .75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5rem;
  color: #0f1111;
  position: relative;
  top: 1.125rem;
  z-index: 2;
  transition: top 0.3s, font-size 0.3s, color 0.3s, transform 0.3s;
}

label.has-value {
  //color: #9e9e9e;
  color: #0f1111;
  -webkit-transform: scale(.8) translateY(-.65em);
  transform: scale(.8) translateY(-.65em);
}

input:focus {
  outline: none;
}

.input-wrapper {
  align-items: center;
  padding: 0!important;
  margin: 0!important;
}
input {
  padding: 1.08rem 0.75rem 0.16rem 0.75rem;
  font-size: 1rem;
  width: 100%;
  border-radius: 0;
  border: 1px solid #E5E7EB;
  outline: 2px solid transparent;
  outline-offset: 2px;
}

input[type=text] {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: #fff;
  width: 100%;
  margin: -17px 0 0;
  //padding: 24px 10px 10px; //
  color: #0f1111;
  position: relative;
  z-index: 1;
  box-sizing: border-box;
  transition: padding-top 0.3s;
}
input[type=text]:focus {
  border-color: #0f1111;
}

.valid{
  border-color: yellowgreen!important;
}

/* CREDIT CARD IMAGE STYLING */
.preload * {
  -webkit-transition: none !important;
  -moz-transition: none !important;
  -ms-transition: none !important;
  -o-transition: none !important;
}

.container {
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
  min-height: 30vw;
  max-height: 35vw;
}

.creditcard svg#card-front,
.creditcard svg#card-back {
  width: 100%;
  -webkit-box-shadow: 1px 5px 6px 0 $main-color;
  box-shadow: 1px 5px 6px 0 $main-color;
  border-radius: 22px;
}

#generate-card {
  font-weight: 400;
  font-size: 12px;
  color: #0f1111;
  padding: 2px 4px;
  background-color: #e9ecef;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  float: right;
  top: -17px;
  z-index: 11;
}
#generate-card:hover{
  color: #fff;
  background-color: #0f1111;
  transition: all .3s ease-in-out;
}
#generate-card:active{
  transform: translateY(5%);
  transition: transform .2s ease-in-out;
}

#eye-icon {
  vertical-align: middle;
  color: #0f1111;
  font-size: 16px;
  opacity: 60%;
  font-weight: 400;
  cursor: pointer;
  position: relative;
  float: right;
  top: 20px;
  right: 5px;
  //margin-top: 15px;
  z-index: 11;
}
#eye-icon:hover{
  opacity: 100%;
  transition: all .2s ease-in-out;
}

/* CHANGEABLE CARD ELEMENTS */
.creditcard .light-color,
.creditcard .dark-color {
  -webkit-transition: fill .5s;
  transition: fill .5s;
}

.creditcard .lightblue {
  fill: #03A9F4;
}

.creditcard .lightblue-dark {
  fill: #0288D1;
}

.creditcard .red {
  fill: #ef5350;
}

.creditcard .red-dark {
  fill: #d32f2f;
}

.creditcard .purple {
  fill: #ab47bc;
}

.creditcard .purple-dark {
  fill: #7b1fa2;
}

.creditcard .cyan {
  fill: #26c6da;
}

.creditcard .cyan-dark {
  fill: #0097a7;
}

.creditcard .green {
  fill: #66bb6a;
}

.creditcard .green-dark {
  fill: #388e3c;
}

.creditcard .lime {
  fill: #d4e157;
}

.creditcard .lime-dark {
  fill: #afb42b;
}

.creditcard .yellow {
  fill: #ffeb3b;
}

.creditcard .yellow-dark {
  fill: #f9a825;
}

.creditcard .orange {
  fill: #ff9800;
}

.creditcard .orange-dark {
  fill: #ef6c00;
}

.creditcard .grey {
  fill: #bdbdbd;
}

.creditcard .grey-dark {
  fill: #616161;
}

/* FRONT OF CARD */
#svg-name {
  text-transform: uppercase;
}

#card-front .st2 {
  fill: #FFFFFF;
}

#card-front .st3 {
  font-family: 'Source Code Pro', monospace;
  font-weight: 600;
}

#card-front .st4 {
  font-size: 54.7817px;
}

#card-front .st5 {
  font-family: 'Source Code Pro', monospace;
  font-weight: 400;
}

#card-front .st6 {
  font-size: 33.1112px;
}

#card-front .st7 {
  opacity: 0.6;
  fill: #FFFFFF;
}

#card-front .st8 {
  font-size: 24px;
}

#card-front .st9 {
  font-size: 36.5498px;
}

#card-front .st10 {
  font-family: 'Source Code Pro', monospace;
  font-weight: 300;
}

#card-front .st11 {
  font-size: 16.1716px;
}

#card-front .st12 {
  fill: #4C4C4C;
}

/* BACK OF CARD */
#card-back .st0 {
  fill: none;
  stroke: #0F0F0F;
  stroke-miterlimit: 10;
}

#card-back .st2 {
  fill: #111111;
}

#card-back .st3 {
  fill: #F2F2F2;
}

#card-back .st4 {
  fill: #D8D2DB;
}

#card-back .st5 {
  fill: #C4C4C4;
}

#card-back .st6 {
  font-family: 'Source Code Pro', monospace;
  font-weight: 400;
}

#card-back .st7 {
  font-size: 27px;
}

#card-back .st8 {
  opacity: 0.6;
}

#card-back .st9 {
  fill: #FFFFFF;
}

#card-back .st10 {
  font-size: 24px;
}

#card-back .st11 {
  fill: #EAEAEA;
}

#card-back .st12 {
  font-family: 'Rock Salt', cursive;
}

#card-back .st13 {
  font-size: 37.769px;
}

/* FLIP ANIMATION */
.container {
  perspective: 1000px;
}

.creditcard {
  width: 100%;
  max-width: 400px;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  transition: transform 0.6s 0.6s;
  -webkit-transition: -webkit-transform 0.6s;
  cursor: pointer;
}

#cc-single {
  position: inherit;
  right: 15px;

  vertical-align: middle;
  padding:0;
  width: 100px;
  height: 55px;
  top: 0;
}

.creditcard .front,
.creditcard .back {
  position: absolute;
  width: 100%;
  max-width: 400px;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
  color: #47525d;
}

.creditcard .back {
  -webkit-transform: rotateY(180deg);
  transform: rotateY(180deg);
}

.creditcard.flipped {
  -webkit-transform: rotateY(180deg);
  transform: rotateY(180deg);
  //transition: transform 1s ease-in-out;
}

.related-field{
  padding-left: 0!important;
}

// for phones
@media only screen and (max-width:563px){
  #cc-single {
    top: -9px!important;
  }
}

@media only screen and (max-width:767px){
  #cc-single {
    max-width: 17%!important;
  }
  #card-number-wrapper{
    max-width: 238.5px;
  }
  .container{
    margin-left: 0!important;
    height: 150px!important;
    min-height: 12vw!important;
    max-height: 29vw!important;
  }
}

// for tablets
@media only screen and (min-width:768px) and (max-width:1620px){
  #first-li{
    margin-top: 0!important;
  }
  #cc-single {
    max-width: 19%!important;
  }
  .container{
    height: 140px!important;
    min-height: 12vw!important;
    max-height: 26vw!important;
  }
}

@media only screen and (min-width:1621px){
  #first-li {
    margin-top: 0!important;
  }
  #cc-single {
    max-width: 90%!important;
    top: 12px!important;
  }
  .container{
    max-height: 200px!important;
    height: 25vw!important;
  }
}

</style>

<style lang="scss">

// Any html element is inserted using innerHTML property or v-html directive, its defined class style
// will be ignored and to solve that you need to set its style inside <style> tag that is NOT scoped.

#cc-single > * {
  position: inherit;
  vertical-align: middle;
  overflow-clip-margin: inherit;
  overflow: clip;
  //transform: scale(0.8);
  max-width: 100%!important;
  max-height: 100%!important;
}

.cc-icon {
  vertical-align: middle;
  float: right;
  position: relative;
  opacity: 0.80;
  //height: 38px;
  max-height: 2.613rem;
  margin-top: -41px;
  //width: 60px;
  max-width: 3rem;
  z-index: 10;
}

</style>