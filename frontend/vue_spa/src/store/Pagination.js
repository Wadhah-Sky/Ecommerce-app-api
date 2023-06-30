/*
* Pinia is an improvement library of vuex for vue3 composition API, which is used for state
* management of properties that can be use by multiple components in your project without
* need to use v-slots to pass data or trigger events when a change is made.
*/

import { defineStore, acceptHMRUpdate } from 'pinia';
import {scrollTopSmooth} from "@/assets/javascript/smothScroll";
import {axios} from "@/common/api.axios";
import {range} from "lodash";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const usePaginationStore = defineStore('Pagination', {
  state: () => ({
    pageNumber: 1,
    response: {},
    dataResult: [],
    dataCount: 0,
    page_size: 1,
    range: [],
    dataLoading: false
  }),
  getters: {
    pagesCount: state => Math.ceil(state.dataCount / state.page_size),
  },
  actions: {
    pagesRange() {
      /**
       * Function to make an array of 5 value depending on 'pageNumber', and make sure the start
       * value is not less than zero and end value is not bigger than 'pagesCount' property.
       * Note: the maximum range of array is 5 elements(pages) since we define start with +2
       * and end with -2 from a common dynamic value.
       */

      let start = +this.pageNumber - 2;
      let end = +this.pageNumber + 2;

      if (end > this.pagesCount) {
        start -= (end - this.pagesCount);
        end = this.pagesCount;
      }
      if (start <= 0) {
        end += ((start - 1) * -1);
        start = 1;
      }
      end = end > this.pagesCount ? this.pagesCount : end;
      this.range = range(start, (+end+1)); // since range() count from start to end-1, we add 1 to include the end.
    },
    async changePage(endpoint, pageNumber) {
      /**
       * Function to change state value of 'pageNumber' and trigger getDataResult()
       * by passing endpoint value.
       */

      this.pageNumber = pageNumber;
      await this.getDataResult(endpoint + `?page=${this.pageNumber}`);
    },
    async getDataResult(endpoint) {
      /**
       * Function to retrieve data from backend server using endpoint depending on
       * current state value of 'pageNumber'.
       */

      this.dataLoading = true;
      try {
        this.response = await axios.get(endpoint);
        this.dataCount = this.response.data.count;
        this.dataResult = this.response.data.results;
        this.page_size = this.response.data.page_size;
        this.pagesRange();
      }
      catch (error){
        console.log("Error while trying to retrieve the requested data from backend server!");
        this.pageNumber = 1;
        this.dataResult = [];
      }
      finally {
        this.dataLoading = false;
        // Scroll the browser's window up.
        scrollTopSmooth(window.scrollY, 300, "ease-in-out");
      }
    }
  },
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(usePaginationStore, import.meta.hot))
}