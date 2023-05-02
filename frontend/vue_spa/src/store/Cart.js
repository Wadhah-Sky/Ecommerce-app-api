import { defineStore, acceptHMRUpdate } from 'pinia';
//import {axios} from "@/common/api.axios";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const useCartStore = defineStore('Cart', {
  state: () => ({
    response: {},
    dataResult: [],
    dataLoading: false,
    products: []
  }),
  getters: {
    totalPrice (state) {
      /**
       * Return the sum of price of all items in 'products' array
       */

      // Initialize the total value.
      let total = 0;

      // Check that products array is not empty.
      if (state.products.length > 0) {

        // Loop over 'products' array.
        for (let item of state.products) {
          total += +item.price;
        }

        // Check if total is float number.
        // Note: if value % 1 is equal to 0, means the number is integer.
        if (!((+total % 1) === 0)) {

          // Get the decimal portion of total value.
          let decimalValue = +total % 1;

          // Check that the 'decimalValue' length is more than 2 digits.
          if (String(decimalValue).length > 2) {

            // Get a rounded decimal value of current 'total'.
            // Note: The toFixed() method formats a number using fixed-point notation and return a string value.
            total = Number.parseFloat(String(total)).toFixed(2);
          }
        }

        // Return string of currency and total value.
        return state.products[0]['currencySymbol'] + String(total);
      }
      else {
        return '$0'
      }

    },
    itemsCount (state) {
      /**
       * Return the count of items in 'products' array.
       */

      return state.products.length;
    },
  },
  actions: {
    addItem (obj){
      /**
       * Add new item into the begging of 'products' array.
       */

      // Add the object at the begging of the array.
      this.products.unshift(obj);

      // Store the current 'products' array into local storage api.
      // Note: local storage only work with strings, so we have convert array as json string.
      window.localStorage.setItem("jamie&CassieCart", JSON.stringify(this.products));
    },
    removeItem(index){
      /**
       * Remove an item from 'products' array using the given index.
       */

      this.products.splice(index, 1); // 2nd parameter means remove one item only

      // Store the current 'products' array into local storage api.
      // Note: local storage only work with strings, so we have convert array as json string.
      window.localStorage.setItem("jamie&CassieCart", JSON.stringify(this.products));
    },
    isItemsExists (slug) {
      /**
       * Return true if the given item slug is exists in 'products' array.
       */

      // Loop over 'products' array.
      for (let obj of this.products){
        // Check that the current item (object) slug is equal to given slug
        if(obj.itemS === slug){
          // Return true if condition is true.
          return true;
        }
      }
    },
  }
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useCartStore, import.meta.hot))
}