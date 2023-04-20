import { defineStore, acceptHMRUpdate } from 'pinia';
import {axios} from "@/common/api.axios";
import router from "@/router";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const useProductStore = defineStore('Product', {
  state: () => ({
    response: {},
    dataResult: [],
    selectedProductItem: {},
    productItemsSlugs: {},
    productOptions: {},
    productOptionsCombination: {},
    selectedProductItemOptions: {},
    selectedProductItemSameOptionsStatus: {},
    dataLoading: false,
  }),
  actions: {
    async getDataResult(endpoint) {
      /**
       * Function to retrieve product details from backend server.
       */

      // Change the state of dataLoading.
      this.dataLoading = true;
      try {
        this.response = await axios.get(endpoint);
        this.dataResult = this.response.data;
        this.selectedProductItem = this.dataResult['selected_product_item'];
        this.productOptionsCombination = this.dataResult['available_attributes_combination'];

        if (this.dataResult['related_product_items']){
          // Call the serialize method for product items options.
          await this.serializeProductOptions(this.dataResult['related_product_items']);
        }
        if (this.selectedProductItem['attributes']){
          // Call the set method to selected product item options.
          await this.setSelectedProductItemOptions(this.selectedProductItem['attributes']);
        }

      }
      catch (error){
        await router.replace(
            {
              name: 'page-not-found',
              // preserve current path and remove the first char to avoid the target URL starting with `//`
              params: { pathMatch: router.currentRoute.value.path.substring(1).split('/') },
              // preserve existing query and hash if any
              query: router.currentRoute.value.query,
              hash: router.currentRoute.value.hash
            }
        );
        console.log("Error while trying to retrieve the requested data from backend server!");
        this.response = {}
        this.dataResult = [];
        this.productItem = {};
        this.productItemsSlugs = {};
        this.productOptions = [];
        this.productOptionsCombination = {};
      }
      finally {
        // Whether an error occurred or not, set the state of dataLoading to be false.
        this.dataLoading = false;
      }
    },
    async getProductItemDataResult(endpoint) {
      /**
       * Function to retrieve product item details from backend server.
       */

      // Change the state of dataLoading.
      this.dataLoading = true;

      try {
        let response = await axios.get(endpoint);
        let data = response.data;
        this.selectedProductItem = data['selected_product_item']

        if (this.selectedProductItem['attributes'].length > 0){
          await this.setSelectedProductItemOptions(this.selectedProductItem['attributes']);
        }
      }
      catch (error){
        await router.replace(
            {
              name: 'page-not-found',
              // preserve current path and remove the first char to avoid the target URL starting with `//`
              params: { pathMatch: router.currentRoute.value.path.substring(1).split('/') },
              // preserve existing query and hash if any
              query: router.currentRoute.value.query,
              hash: router.currentRoute.value.hash
            }
        );
        console.log("Error while trying to retrieve the requested data from backend server!");
        this.selectedProductItem = {};
      }
      finally {
        // Whether an error occurred or not, set the state of dataLoading to be false.
        this.dataLoading = false;
      }
    },
    async serializeProductOptions(arrayOfObj) {
      /**
       * Method to serialize product items options.
       */

      // Initialize an empty object.
      let options = {};
      let sameOptionsStatus = {};
      let productItemsSlugs = {};

      // Create 2D array where rows length are equal to 'arrayOfObj.length'.
      // let combination = [...Array(arrayOfObj.length)].map(() => Array(0));

      // Loop over the array of objects.
      for (let obj of arrayOfObj ){

        // Get the current looped object 'attributes' object.
        let attributesObj = obj.attributes;

        // Set the current product item slug as key with attributes empty array as value.
        productItemsSlugs[obj.slug] = [];

        // Loop over the attribute object.
        /*
          Notice: if loop over object, the (key) will represent the 'index' of loop
                  while the 'value' of the loop will represent the (value) of that (key).
         */
        for (let key in attributesObj){

          // Make sure to not store duplicated keys in 'options'.
          if (! options[key]){
            // store the key with value of empty array.
            options[key] = [];
          }

          // Check if value of current key is have array of more than one item or not.
          if (!sameOptionsStatus[key] && attributesObj[key].length > 1) {
            // Push an object of key: true as sign that this key have array of multiple items.
            // This option is useful for multi-select component to set :multi attribute as true.
            sameOptionsStatus[key] = true;
          }

          // Loop over the value (array of objects) of current key of attribute objects.
          for (let value of attributesObj[key]){

            /*
              Note: use map() method to loop over array of objects, and select specific key
              in that object, then find the object index using indexOf() for specific value.
             */
            // Push non-duplicated object to the array value of key, when the return value of 'indexOF()' is (-1).
            if (options[key].map(object => object.value).indexOf(value.child_attribute) === -1){

              // Push specific value 'child_attribute' of looped item object.
              options[key].push(
                  {
                    'value': value.child_attribute,
                    'parentAttribute': value.parent_attribute,
                    'thumbnail': value.thumbnail,
                    $isDisabled: false
                  }
              );

            }

            // Push the current 'value.child_attribute' to its related product item object slug.
            productItemsSlugs[obj.slug].push(value.child_attribute);

          }
        }
      }

      // Set value of 'productOptions'.
      this.productOptions = options;
      // Set value of 'selectedProductItemSameOptionsStatus'.
      this.selectedProductItemSameOptionsStatus = sameOptionsStatus;
      // Set value of 'productItemsSlugs'.
      this.productItemsSlugs = productItemsSlugs;
    },
    async setSelectedProductItemOptions(attributesObj){
      /**
       * Method to set state of 'selectedProductItemOptions'
       */

      // Initialize an empty object.
      let options = {};

      // Loop over the attribute object.
      /*
         Notice: if loop over object, the (key) will represent the 'index' of loop
                 while the 'value' of the loop will represent the (value) of that (key).
       */
      for (let key in attributesObj){

        // Make sure to not store duplicated keys in 'options'.
        if (! options[key]){
          // store the key with value of empty array.
          options[key] = [];
        }

        // Loop over array of 'attributesObj[key]'
        for (let item of attributesObj[key]){

          /*
              Note: use map() method to loop over array of objects, and select specific key
              in that object, then find the object index using indexOf() for specific value.
           */
          // Push non-duplicated object to the array value of key, when the return value of 'indexOF()' is (-1).
          if (options[key].map(object => object.value).indexOf(item) === -1){
            // Push value of looped item of array.
            options[key].push({'value': item, $isDisabled: false});
          }
        }
      }

      // Set value of 'selectedProductItemOptions'.
      this.selectedProductItemOptions = options;
    }
  }
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useProductStore, import.meta.hot))
}