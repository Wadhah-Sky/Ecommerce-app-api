import { defineStore, acceptHMRUpdate } from 'pinia';


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const useEndpointStore = defineStore('Endpoint',{
    state: () => ({
        homeEndpoint: '/api/v1/home/',
        storeCategoryDetailsEndpoint: '/api/v1/store/category/details/',
        storeCategoriesEndpoint: '/api/v1/store/categories/',
        storeProductsEndpoint: '/api/v1/store/products/category/',
        storeAttributesEndpoint: '/api/v1/store/attributes/category/',
        storeProductDetailsEndpoint: '/api/v1/product/details/',
        cartCheckEndpoint: '/api/v1/cart/check/',
        shippingCountiesEndpoint: '/api/v1/shipping/countries/',
        shippingMethodsEndpoint: '/api/v1/shipping/methods/',
        shippingCostEndpoint: '/api/v1/shipping/cost/',
        paymentMethodsEndpoint: '/api/v1/payment/methods/',
    }),
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useEndpointStore, import.meta.hot))
}