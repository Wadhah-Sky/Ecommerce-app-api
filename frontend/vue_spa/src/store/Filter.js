import { defineStore, acceptHMRUpdate } from 'pinia';
import {axios} from "@/common/api.axios";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const useFilterStore = defineStore('Filter', {
  state: () => ({
    collapsed: false,
    response: {},
    dataResult: [],
    dataLoading: false,
    availableColorOptions: [
        'blacks', 'greys', 'white', 'browns', 'beige', 'reds', 'pinks', 'oranges',
        'yellows', 'ivory', 'greens', 'blues', 'purples', 'golds', 'silvers',
        'multi', 'clear'
    ],
    checkedOptions: [],
    price: {minPrice: undefined, maxPrice: undefined},
    availableSelectByOptions: [
        { option: 'Deals', value: 'deals' },
        { option: 'Price: Low to High', value: 'price-low-to-high' },
        { option: 'Price: High to Low', value: 'price-high-to-low' },
    ],
    selectByOption: null
  }),
  getters: {
  },
  actions: {
    toggleCollapsedState (){
      /**
       * Function to reverse the state of collapsed for side panel.
       */
      // Note: if collapsed value is false means the sidepanel is closing/closed.
      this.collapsed = !this.collapsed;
    },
    async getDataResult(endpoint) {
      /**
       * Function to retrieve all filters options from backend server.
       */

      // Change the state of dataLoading.
      this.dataLoading = true;
      try {
        this.response = await axios.get(endpoint);
        this.dataResult = this.response.data;
      }
      catch (error){
        // console.log(error.response.statusText)
        // console.log("Error while trying to retrieve the requested data from backend server!");
        this.response = {}
        this.dataResult = [];
      }
      finally {
        // Whether an error occurred or not, set the state of dataLoading to be false.
        this.dataLoading = false;
      }
    },
  }
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useFilterStore, import.meta.hot))
}