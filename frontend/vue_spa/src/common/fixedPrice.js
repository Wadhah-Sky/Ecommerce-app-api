const priceFix = (amount, returnedType=String, decimalDigits=2, int=true) => {
    /**
     * Method to return fixed price with two digit of decimal if it has decimal value OR
     * in case 'int' parameter set true.
     *
     * @param {String, Number} amount The value to fix.
     * @param {Object} returnedType The type object of returned value, default: String.
     * @param {Number} decimalDigits Set the required decimal digits to be fixed for, default: 2.
     * @param {Boolean} int The flag that means implement this method on integer (without decimal) values, default: True.
     *
     */

    // Note: if (value % 1) is equal to 0, means the number is integer. OR 'int' is true.
    if (!((+amount % 1) === 0) || int === true) {

        // Get the decimal portion of amount value.
        let decimalValue = +amount % 1;

        // Check that the 'decimalValue' length is more than required decimal digits. OR 'int' is true.
        if (String(decimalValue).length > Number(decimalDigits) || int === true) {

            // Get a rounded decimal value of current 'amount'.
            // Note: The toFixed() method formats a number using fixed-point notation and return a string value.
            amount = Number.parseFloat(String(amount)).toFixed(decimalDigits);
        }
    }

    // Return the original amount value or the fixed.
    return returnedType(amount)
};

export {priceFix}