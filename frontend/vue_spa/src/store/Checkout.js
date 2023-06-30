import { defineStore, acceptHMRUpdate } from 'pinia';
import {priceFix} from "@/common/fixedPrice";
import {axios} from "@/common/api.axios";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

/*
  Info: We are using following terms to mention prices:
        1- total: is the total price of cart items without counting the quantity.
        2- subtotal: it's any price multiplied by certain quantity.
        3- grand total: it's the overall price of order that take in concern the discounts and taxing amount.
 */

export const useCheckoutStore = defineStore('Checkout', {
  state: () => ({
    response: {},
    dataResult: [],
    dataLoading: false,
    cartProducts: [],
    cartApiCouponCode: '',
    cartApiPriceCurrencySymbol: '$',
    cartApiTotalDiscountAmount: 0,
    cartApiTotalPriceAmount: 0,
    cartApiErrorMsg: '',
    showCartDropDownMenu: false,
    shippingDetails: {},
    countries: [],
    shippingMethods: [],
    shippingApiPriceCurrencySymbol: '$',
    shippingApiCostPriceAmount: 0,
    shippingApiErrorMsg: '',
    paymentDetails: {},
    paymentMethods: []
  }),
  getters: {
    cartItemsQuantity (state){
      /**
       * Return the total cart items quantity object:
       * {<sku>: <quantity>, ...}
       */

      let quantity = {};

      // Loop over cart products
      for (let item of state.cartProducts) {
        // Set value of quantity of each product item, use item 'sku' as key.
        quantity[item.sku] = item.quantity;
      }

      return quantity;
    },
    cartTotalQuantity () {
      /**
       * Return the number of overall quantity object
       */

      let total = 0;

      // Loop over quantity object.
      for (let val of Object.values(this.cartItemsQuantity)) {
        total += val;
      }

      return total;
    },
    cartTotalPriceAmount (state) {
      /**
       * Return the sum amount of price of all items without quantity in 'cartProducts' array
       */

      // Initialize the total value.
      let total = 0.00;

      // Check that products array is not empty.
      if (state.cartProducts.length > 0) {

        // Loop over 'products' array.
        for (let item of state.cartProducts) {
          total += +item.priceAmount;
        }

      }
      // Return string total value.
      return priceFix(total);
    },
    cartTotalQuantityPriceAmount (state) {
      /**
       * Method to calculate the total amount of each product price multiplied by its quantity.
       */

      // Otherwise calculate the total price on frontend.

      let total = 0.00;
      let quantity = this.cartItemsQuantity;

      // Loop over cart products.
      for (let item of state.cartProducts) {
        // Note: itemSubtotal() method return a string value.
        total += +this.itemSubtotal(item.priceAmount, quantity[item.sku]);
      }

      return priceFix(total);
    },
    cartTotalQuantityPriceAmountWithDiscount (state) {
      /**
       * Method to calculate the total amount of each product price multiplied by its quantity
       * including discount if available.
       */

      // check if we have total price from backend server then return it.
      if (![undefined, '', null, 0].includes(state.cartApiTotalPriceAmount)) {
        return state.cartApiTotalPriceAmount;
      }
      else {
        return this.cartTotalQuantityPriceAmount;
      }
    },
    checkoutGrandTotalPriceAmount(state) {
      /**
       * Calculate grand total price amount that include shipping cost, tax and cart subtotal price amount.
       */

      return priceFix(this.cartTotalQuantityPriceAmountWithDiscount + (+state.shippingApiCostPriceAmount));
    },
    itemsCount(state) {
      /**
       * Return the count of items in 'cartProducts' array.
       */

      return state.cartProducts.length;
    },
    cartItemsSkuString (state) {
      /**
       * Return a joined string of all cart product items sku.
       */

      // Initialize an empty array.
      let arr = []

      // Loop over 'products'
      for (let item of state.cartProducts){
        // Push current item sku into array.
        arr.push(item.sku);
      }

      // join array items as string seperated by comma (,)
      return arr.join();
    },
    shippingAddress(state) {
      /**
       * Return the shipping address object. the return object contains:
       * country_iso_code, region, city, postal_code
       */

      return {
        "country_iso_code": state.shippingDetails['country'] || '',
        "region": state.shippingDetails['region'] || '',
        "city": state.shippingDetails['city'] || '',
        "postal_code": state.shippingDetails['postalCode'] || ''
      }
    },
    isShippingInfoSet(state) {
      /**
       * Method to return true if certain required shipping address and shipping method are set,
       * useful to trigger cost calculation from backend server.
       */

      // Set required values.
      let shippingAddress = Object.values(state.shippingAddress);
      let shippingMethod = state.shippingDetails['shippingMethod'] || '';

      // Check that if shipping method is set.
      if (![undefined, '', null].includes(shippingMethod)) {

        // Return false of first array is contain at least one item from selected array items,
        // otherwise return true.
        return ![undefined, '', null].some(e => shippingAddress.includes(e));
      }
      else {
        return false
      }
    },
    isShippingDetailsSet (state){
      /**
       * Method to return true if all required shipping details are set, useful to watch shipping details.
       */

      // check if required shipping info is set.
      if (state.isShippingInfoSet) {

        // Set required values.
        let firstName = state.shippingDetails['firstName'] || '';
        let lastName = state.shippingDetails['lastName'] || '';
        let email = state.shippingDetails['email'] || '';
        let phoneNumber = state.shippingDetails['phoneNumber'] || '';
        let address1 = state.shippingDetails['address1'] || '';

        // let shippingMethod = state.shippingDetails['shippingMethod'] || '';
        // let shippingAddress = Object.values(state.shippingAddress);
        // Merge array of 'shippingAddress' with array of other details.
        // let mergeResult = [...[shippingMethod, address1, phoneNumber, firstName, lastName, email], ...shippingAddress];

        let result = [firstName, lastName, email, phoneNumber, address1]

        // Return false of first array is contain at least one item from selected array items,
        // otherwise return true.
        return ![undefined, '', null].some(e => result.includes(e));
      }
      else{
        return false;
      }
    }
  },
  actions: {
    saveCart(cart){
      /**
       * Method to store cart object in browser local storage that related to this website domain.
       */

      // Store the current 'cartProducts' array into local storage api.
      // Note: local storage only work with strings, so we have convert array as json string.
      window.localStorage.setItem("jamie&CassieCart", JSON.stringify(cart));
    },
    addItem (obj){
      /**
       * Add new item at the begging of 'cartProducts' array.
       */

      // Loop over 'cartProducts' array as [index, val]
      // products should be=> [{}, {}...]
      for (let [index, val] of this.cartProducts.entries()){
        // Check that if current item property 'itemS' is equal to the given object 'itemS'.
        if(val.itemS === obj.itemS){
          // Remove the current item from the 'products' array.
          this.cartProducts.splice(index, 1); // 2nd parameter means remove one item only
        }
      }

      // Add the given object at the begging of the array.
      this.cartProducts.unshift(obj);

      // Store cart products into local storage.
      this.saveCart(this.cartProducts);
    },
    removeItem(index){
      /**
       * Remove an item from 'cartProducts' array using the given index.
       */

      this.cartProducts.splice(index, 1); // 2nd parameter means remove one item only

      // Store cart products into local storage.
      this.saveCart(this.cartProducts);
    },
    updateItemQuantity(sku, quantity=1){
      /**
       * Update certain product in 'cartProducts' quantity.
       */
      for (let item of this.cartProducts){
        if(item.sku === sku){
          item.quantity = quantity;
          break;
        }
      }
    },
    isItemExist (slug) {
      /**
       * Return true if the given item slug is exists in 'products' array.
       */

      // Loop over 'cartProducts' array.
      for (let obj of this.cartProducts){
        // Check that the current item (object) slug is equal to given slug
        if(obj.itemS === slug){
          // Return true if condition is true.
          return true;
        }
      }
    },
    itemSubtotal(priceAmount, quantity=1) {
      /**
       * Return the price amount after multiplied by certain quantity.
       */

      // Get total value.
      let total = +priceAmount * +quantity;

      return priceFix(total);
    },
    async cartCheck(endpoint, data){
      /**
       * Method to make HTTP POST request to backend server in order to check
       * given data and get response.
       *
       * @param {String} endpoint the backend api endpoint.
       * @param {Object} data the json object to send with HTTP POST request.
       */

      this.dataLoading = true;

      try{
        let response = await axios.post(endpoint, data);
        this.cartApiErrorMsg = '';
        this.cartApiCouponCode = response.data['coupon_title'];
        this.cartApiPriceCurrencySymbol = response.data['price_currency_symbol'];
        this.cartApiTotalDiscountAmount = response.data['total_discount_amount'];
        this.cartApiTotalPriceAmount = response.data['total_price_amount'];
      }
      catch (error){
        this.cartApiErrorMsg = error.response.data['message'];
      }
      finally {
        this.dataLoading = false;
      }
    },
    resetCartApiState () {
      /**
       * Method to reset cart api related states.
       */

      this.cartApiErrorMsg = '';
      this.cartApiCouponCode = '';
      this.cartApiPriceCurrencySymbol = '$';
      this.cartApiTotalDiscountAmount = 0;
      this.cartApiTotalPriceAmount = 0;
    },
    async refreshCartItems (endpoint){
      /**
       * Method to update items in 'cartProducts' with new data and remove any
       * item is not exist in received data from backend server.
       */

      // check that current 'cartProducts' state is not an empty array.
      if (this.cartProducts.length > 0) {

        this.dataLoading = true;

        // Get the joined string of cart items 'sku'
        let skuStr = this.cartItemsSkuString;

        try {
          let response = await axios.get(endpoint + '?items_sku=' + skuStr);

          // Initialize an empty array.
          let updatedProducts = [];

          // Loop over 'products'
          for (let obj of this.cartProducts) {

            // Loop over the returned response data array.
            for (let [index, item] of response.data.entries()) {

              // Check that the current item 'sku' of data response array is the same
              // current item (object) of 'products';
              if (item['sku'] === obj.sku) {

                // Set the price amount of item.
                let itemPriceAmount = ['', null, undefined, 0].includes(item['deal_price_amount']) ?
                    item['list_price_amount'] : item['deal_price_amount'];

                // Update the wanted details with the new ones.
                obj.itemS = item['slug'];
                obj.limitPerOrder = item['limit_per_order'];
                obj.thumbnail = item['thumbnail'];
                obj.currencySymbol = item['price_currency_symbol'];
                obj.priceAmount = itemPriceAmount;
                // Set quantity of current item as 1 if it's bigger than limit per order for same item.
                if (obj.quantity > obj.limitPerOrder) {
                  obj.quantity = 1;
                }

                // Push the current item (the updated object) of 'products' to 'updatedProducts' array.
                updatedProducts.push(obj);

                // Remove the current item of data response, for more efficiency.
                response.data.splice(index, 1); // 2nd parameter means remove one item only

                // Break the loop of data response.
                break;
              }
            }
          }

          // Set the updated array to the exist array of 'products'
          this.cartProducts = updatedProducts;

          // Store cart products into local storage.
          this.saveCart(this.cartProducts);

        }
        catch (error) {
          console.log("Error while trying to retrieve the requested data from backend server!");
        }
        finally {
          this.dataLoading = false;
        }
      }
    },
    async saveShippingDetails(infoObj) {
      /**
       * Method to store shipping details object in browser local storage that related to this website domain.
       */

      // Store the current 'shippingDetails' object into local storage api.
      // Note: local storage only work with strings, so we have convert array as json string.
      window.localStorage.setItem("jamie&CassieShippingDetails", JSON.stringify(infoObj));
    },
    async setShippingDetails (key, val){
      /**
       * Method to set customer shipping details object
       */

      if (![null, undefined, ''].includes(key) && ![null, undefined].includes(val)) {
        // set key and its value in 'shippingDetails'
        this.shippingDetails[key] = val;

        // Save shippingDetails object into local storage.
        await this.saveShippingDetails(this.shippingDetails);

      }
    },
    async getDataResult(endpoint){
      /**
       * Method to retrieve data from backend server.
       */
      this.dataLoading = true;

      try{
        let response = await axios.get(endpoint);
        return response.data
      }
      catch (error) {
        console.log("Error while trying to retrieve the requested data from backend server!");
      }
      finally {
        this.dataLoading = false;
      }
    },
    async getCounties (endpoint){
      /**
       * Method to retrieve countries that available.
       */

      this.countries = await this.getDataResult(endpoint);
    },
    async getShippingMethods (endpoint){
      /**
       * Method to retrieve shipping methods that available to ship with.
       */

      this.shippingMethods = await this.getDataResult(endpoint);
    },
    async shippingCost(endpoint, data){
      /**
       * Method to make HTTP POST request to backend server in order to check
       * given data and get response.
       *
       * @param {String} endpoint the backend api endpoint.
       * @param {Object} data the json object to send with HTTP POST request.
       */

      this.dataLoading = true;

      try{
        let response = await axios.post(endpoint, data);
        this.shippingApiErrorMsg = '';
        this.shippingApiPriceCurrencySymbol = response.data['price_currency_symbol'];
        this.shippingApiCostPriceAmount = response.data['shipping_cost_amount'];
      }
      catch (error){
        this.shippingApiErrorMsg = error.response.data['message'];
      }
      finally {
        this.dataLoading = false;
      }
    },
    resetShippingApiState () {
      /**
       * Method to reset shipping api related states.
       */

      this.shippingApiErrorMsg = '';
      this.shippingApiPriceCurrencySymbol = '$';
      this.shippingApiCostPriceAmount = 0;
    },
    async getPaymentMethods (endpoint){
      /**
       * Method to retrieve payment methods that available to pay with.
       */

      this.paymentMethods = await this.getDataResult(endpoint);
    },
    async savePaymentDetails(infoObj) {
      /**
       * Method to store payment details object in browser local storage that related to this website domain.
       */

      // Store the current 'paymentDetails' object into local storage api.
      // Note: local storage only work with strings, so we have convert array as json string.
      window.localStorage.setItem("jamie&CassiePaymentDetails", JSON.stringify(infoObj));
    },
    async setPaymentDetails (key, val){
      /**
       * Method to set customer payment details object
       */

      if (![null, undefined, ''].includes(key) && ![null, undefined].includes(val)) {
        // set key and its value in 'paymentDetails'
        this.paymentDetails[key] = val;

        // Save shippingDetails object into local storage.
        await this.savePaymentDetails(this.paymentDetails);

      }
    },
    isPaymentCard(val) {
      /**
       * Method to return true if provided value is payment card method otherwise return false.
       */

      let isCard = false;

      for (let obj of this.paymentMethods){
        if(obj.value === val){
          isCard = obj['is_card'];
          break;
        }
      }
      return isCard;
    }
  }
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useCheckoutStore, import.meta.hot))
}