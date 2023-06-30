import { useIMask, IMask } from 'vue-imask';
import moment from 'moment';


// Initialize new date object.
let date = new Date();
// Note: in javascript Date, the month indexing start from zero.
// Note: we need the card to be active in the next month of current date, so we increase the month by one.
// const currentMonth = (date.getMonth() + 1) + 1 ;
// We need the only last two digits of the year of current date.
const currentYear = date.getFullYear() % 100;
const momentFormat = 'MM/YY';

/*
  Note: For date mask, if you set 'pattern' option, then you also have to provide format
        and parse options.
        Also Date mask uses independent pattern blocks, so it's possible to input nonexistent
        dates until mask is complete. When last character is inserted then input is converted
        to Date object and get verified. This leads to weird situations when you might have
        incorrect day, but not being able to insert year. It is not possible to validate Date
        intermediate states in general way, but you still can use validate callback on application
        side to check your specific case.
 */

/*
  Important: The must important part of InputMask class is 'mask' property, this property responsible
             to allow entering value if valid and trigger @accept/@complete events.
 */
const cardExpireDateProps = {
    mask: Date,
    regex: /^(?=.{0,5}$)((0[1-9]|1[0-2])\/?([0-9]{2})$)/,
    // other options are optional
    pattern: momentFormat,  // Pattern mask with defined blocks, default is 'd{.}`m{.}`Y'
    // you can provide your own blocks definitions, default blocks for date mask are:
    blocks: {
        MM: {
            mask: IMask.MaskedRange,
            from: 1,
            to: 12,
            maxLength: 2,
        },
        YY: {
            mask: IMask.MaskedRange,
            from: currentYear,
            to: currentYear + 5,
            maxLength: 2,
        }
    },
    // define date -> str conversion
    format: (date) => {
        return moment(date).format(momentFormat);
    },
    // define str -> date conversion
    parse: (str) => {
        return moment(str, momentFormat);
    },

    // optional interval options
    // Note: in javascript Date, the month indexing start from zero.
    // min: new Date(2023, 0, 1),  // defaults to `1900-01-01`
    // max: new Date(2099, 0, 1),  // defaults to `9999-01-01`

    autofix: true,  // defaults to `false`

    // placeholderChar: '#',  // defaults to '_'

    /*
       Note: for Date mask, if 'lazy' option set to false will show placeholder e.g. __/__
             and update placeholder of the mask in the input field with every
             character insert from the user.
             Also, if you set range between blocks property and that range have static digit
             then will show as static value in the input field.
     */
    lazy: true, // defaults to `true`

    /*
       Note: if 'overwrite' option set to true will enable characters overwriting in the
             input field (replace) instead of inserting, also it is possible to set to 'shift'
             means shift value of input field to the right if new value insert in the left.
     */
    overwrite: true  // defaults to `false`
};

const cardNameProps = {
    mask: /^(?=.{0,20}$)(?!\s)((?:[A-Za-z]+\s?){1,3}$)/,
    regex: /^(?=.{0,20}$)(?!\s)((?:[A-Za-z]+\s?){1,3}$)/,
    // skip invalid is by default is true, means don't write the character
    // that invalid to mask value.
    skipInvalid: true,
    // Lazy option is to lazy overwrite of placeholder if has been set to false.
    lazy: true
};

const cardNumberProps = {
    mask: [
        {
            mask: '0000 000000 00000',
            regex: '^3[47]\\d{0,13}',
            cardType: 'american express'
        },
        {
            mask: '0000 0000 0000 0000',
            regex: '^(?:6011|65\\d{0,2}|64[4-9]\\d?)\\d{0,12}',
            cardType: 'discover'
        },
        {
            mask: '0000 000000 0000',
            regex: '^3(?:0([0-5]|9)|[689]\\d?)\\d{0,11}',
            cardType: 'diners'
        },
        {
            mask: '0000 0000 0000 0000',
            regex: '^(5[1-5]\\d{0,2}|22[2-9]\\d{0,1}|2[3-7]\\d{0,2})\\d{0,12}',
            cardType: 'mastercard'
        },
        // {
        //     mask: '0000-0000-0000-0000',
        //     regex: '^(5019|4175|4571)\\d{0,12}',
        //     cardType: 'dankort'
        // },
        // {
        //     mask: '0000-0000-0000-0000',
        //     regex: '^63[7-9]\\d{0,13}',
        //     cardType: 'instaPayment'
        // },
        {
            mask: '0000 000000 00000',
            regex: '^(?:2131|1800)\\d{0,11}',
            cardType: 'jcb15'
        },
        {
            mask: '0000 0000 0000 0000',
            regex: '^(?:35\\d{0,2})\\d{0,12}',
            cardType: 'jcb'
        },
        {
            mask: '0000 0000 0000 0000',
            regex: '^(?:5[0678]\\d{0,2}|6304|67\\d{0,2})\\d{0,12}',
            cardType: 'maestro'
        },
        // {
        //     mask: '0000-0000-0000-0000',
        //     regex: '^220[0-4]\\d{0,12}',
        //     cardType: 'mir'
        // },
        {
            mask: '0000 0000 0000 0000',
            regex: '^4[0-9]{12}(?:[0-9]{3})?$',
            cardType: 'visa'
        },
        {
            mask: '0000 0000 0000 0000',
            regex: '^62\\d{0,14}',
            cardType: 'union pay'
        },
        {
            mask: '0000 0000 0000 0000',
            regex: '^(?=.{0,19}$)(?!\\s)([0-9]*\\s?){1,4}$',
            cardType: 'unknown'
        }
    ],
    dispatch: function (appended, dynamicMasked) {
        let number = (dynamicMasked.value + appended).replace(/\D/g, '');

        for (let i = 0; i < dynamicMasked.compiledMasks.length; i++) {
            let re = new RegExp(dynamicMasked.compiledMasks[i].regex);
            //console.log("Value:", number, number.match(re))
            if (number.match(re) !== null) {

                return dynamicMasked.compiledMasks[i];
            }
        }
    }
};

const cardSecurityCodeProps = {
    /*
      Info: For MasterCard, Visa, and Discover cards, the security code is the three-digit code
            located on the back of the card. For American Express cards, it's the four-digit code
            located on the right side of the front of the card.
     */
    /*
      Note: if you put '0000' as mask, the inputMask element will trigger @complete event only if
            there are 4 matched digits in the input field, so we set mask the same as regex value BUT
            since we are using 'displayChar' property we can't do it.
            Also mask can be use as static placeholder.
     */

    /*
       Info: '0' means any digit, also other options:

              where definitions are:

              0 - any digit
              a - any letter
              * - any char

              other chars which is not in custom definitions supposed to be fixed

              [] - make input optional
              {} - include fixed part in unmasked value
              ` - prevent symbols shift back
     */
    // We were using this regex: /^(?=.{3,4}$)(?!\s)[0-9]$/
    // Here we are using dynamic select mask by specify array of masks.
    mask: [
        {
            mask: '000',
            regex: /^[0-9]{3}$/,
            // Secure text entry.
            displayChar: '*',
        },
        {
            mask: '0000',
            regex: /^[0-9]{4}$/,
            // Secure text entry.
            displayChar: '*',
        }
    ]
};

const cardSecurityNoSecretCodeProps = {
    mask: [
        {
            mask: '000',
            regex: /^[0-9]{3}$/,
            // Secure text entry, null.
            displayChar: '',
        },
        {
            mask: '0000',
            regex: /^[0-9]{4}$/,
            // Secure text entry, null.
            displayChar: '',
        }
    ],
};


const cardPaymentMask = (fieldName='') => {
    /**
     * Method to return object contains multiple reactive objects:
     *
     * {el: RefImpl, mask: Proxy(RefImpl), masked: RefImpl, unmasked: RefImpl, typed: RefImpl}
     *
     * 1- one for imask input and
     * 2- second the mask of that input object.
     *
     * @param {String} fieldName The field name that will be used to set the appropriate imask input with its mask.
     */

    /*
      IMPORTANT: You should not set the useIMask() method inside an async block, will return undefined errors.
     */

    let field = String(fieldName);
    let imaskObj = null;

    // Note: You can't set 'const' or 'let' statement inside (case) of (switch) statement.
    if (field === 'cardExpireDate') {

        // imaskObj = useIMask({
        //     mask: 'MM{/}YY',
        //     // you can provide your own blocks definitions, default blocks for date mask are:
        //     blocks: {
        //         MM: {
        //             mask: IMask.MaskedRange,
        //             from: 1,
        //             to: 12,
        //             maxLength: 2,
        //         },
        //         YY: {
        //             mask: IMask.MaskedRange,
        //             from: 23,
        //             to: 99,
        //             maxLength: 2,
        //         },
        //     },
        // });

        /*
          Note: useImask() method return two reactive (as ref()) objects:
                1- el: this is the input imask object and can be set to ref attribute for <input ref="el">
                2- mask: this the mask object and can be used to access input imask values, if you choose
                         not to use 'el' object as ref then you can do something like:

                         <input v-imask="mask" />
                         <imask-component :mask="mask" />
          */
        imaskObj = useIMask(cardExpireDateProps);
    }
    else {
        switch (field) {
            case 'cardName':

                imaskObj = useIMask(cardNameProps);
                break;
            case 'cardNumber':

                imaskObj = useIMask(cardNumberProps);
                break;
            case 'cardSecurityCode':

                imaskObj = useIMask(cardSecurityCodeProps);
                break;
            case 'cardSecurityNoSecretCode':

                imaskObj = useIMask(cardSecurityNoSecretCodeProps);
                break;
        }
    }

    // Info: imaskObj in real looks:
    // {el: RefImpl, mask: Proxy(RefImpl), masked: RefImpl, unmasked: RefImpl, typed: RefImpl}
    return imaskObj;
};

export {
    cardNameProps,
    cardExpireDateProps,
    cardNumberProps,
    cardSecurityCodeProps,
    cardSecurityNoSecretCodeProps,
    cardPaymentMask
};
