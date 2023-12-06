import { defineStore, acceptHMRUpdate } from 'pinia';
import {useContentLoadingStore} from "@/store/ContentLoading";
import {axios} from "@/common/api.axios";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const useHomeStore = defineStore('Home',{
    state: () => ({
        response: {},
        dataResult: [],
    }),
    actions: {
    async getDataResult(endpoint) {
      /**
       * Function to retrieve all homepage data from backend server.
       */

      try {
        this.response = await axios.get(endpoint);
        this.dataResult = this.response.data;
      }
      catch (error){
          // console.log("Error while trying to retrieve the requested data from backend server!");
          // console.log(error.response.statusText);
      }
      finally {
          /*
              Note: if one store uses another store, you can directly import and call the useStore()
              function within actions and getters. Then you can interact with the store just like
              you would from within a Vue component.
            */
          const storeContentLoading = useContentLoadingStore();
          // Set state of homeViewDataLoading to be false so the user can view the content of home page.
          // Note: We need to delay this step so that the 'LogoLoadingComponent' still active for longer time.
          setTimeout(() => {storeContentLoading.$patch({homeViewDataLoading: false})},0);
      }
    },

  }

});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useHomeStore, import.meta.hot))
}