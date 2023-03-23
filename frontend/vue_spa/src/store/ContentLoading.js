import { defineStore, acceptHMRUpdate } from 'pinia';


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

export const useContentLoadingStore = defineStore('ContentLoading', {
  state: () => ({
    homeViewDataLoading: true,
    navSidebarDataLoading: true
  })
});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
    import.meta.hot.accept(acceptHMRUpdate(useContentLoadingStore, import.meta.hot))
}