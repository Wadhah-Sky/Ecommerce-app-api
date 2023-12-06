import { defineStore, acceptHMRUpdate } from 'pinia';
import NavSidebarSeperatorComponent from "@/components/NavSidebarSeperatorComponent";
import {useContentLoadingStore} from "@/store/ContentLoading";
import {axios} from "@/common/api.axios";
import router from "@/router";
import {shallowRef} from "vue";


/*
* state: for storing your reactive data properties.
* getters: are methods that equivalent to computed properties, which means only change
*          when the state of reactive property is changed, can be used to make changing
*          on state properties without change the original value.
* actions: methods are synchronized by default and can be asynchronous, can be used
*          to change the state of reactive property.
*/

/*
 Info: Unlike ref(), the inner value of a shallow ref is stored and exposed as-is, and will not be made
       (deeply) reactive. To reduce reactivity overhead for Large immutable structures like components or
       big arrays that contains thousands of objects.
*/
const seperatorComponent = shallowRef(NavSidebarSeperatorComponent);

export const useNavSidebarStore = defineStore('NavSidebar',{
    state: () => ({
        response: {},
        navSidebarTheme: 'white-theme',
        dynamicNavArray:[],
        menu: [],
        show: false,
        collapsed: true
    }),
    actions: {
        toggleNavSidebarView() {
            /**
             * Toggle the Nav sidebar view state
             */

            // Important: first you should toggle value of 'collapsed' in the nav sidebar store, then
            //            toggle value of hide in the same store.
            this.collapsed = !this.collapsed;
            this.show = !this.show;
        },
        addHeaderNavigation(text){
            /**
             * Function to add details for header object into the 'menu' array.
             */

            this.menu.push({
                header: text,
                hiddenOnCollapse: true
            });
        },
        addNavigation(array) {
             /**
             * Function that received an array of objects that we will loop over it and push each item
             * into the 'menu' array.
             */

            /* We use 'of' keyword to represent the element of array not the index
               value for that element like we do when use 'in' keyword. */
            for (let item of array){
                this.menu.push(item)
            }
        },
        addSeperator(){
            /**
             * Functon to push a seperator component as object into 'menu' array.
             */

            this.menu.push({
                component: seperatorComponent
            });
        },
        addChildArray(categoryArray){
            /**
             * Function to add child objects to certain parent object of 'menu' array.
             */

            const result = [];
            for (let item of categoryArray){
                result.push({
                    href: `/store/category/${item.slug}?page=1`,
                    title: item.title,
                    exact: true
                })
            }
            return result
        },
        addDynamicImageNavigation() {
            /**
             * Function to add items of 'dynamicNavArray' these have an image as objects using
             * <img> element into 'menu' array.
             */

            for (let item of this.dynamicNavArray) {
                if (item.thumbnail) {
                    this.menu.push({
                        title: item.title,
                        icon: {
                            element: 'img',
                            attributes: {
                                src: item.thumbnail,
                            }
                        },
                        child: this.addChildArray(item.leaf_nodes),
                        exact: true
                    });
                }

            }
        },
        addDynamicIconNavigation() {
            /**
             * Function to add items of 'dynamicNavArray' those have an icon as objects using
             * awesome font class into 'menu' array.
             */
            for (let item of this.dynamicNavArray) {
                if (item.icon){
                    this.menu.push({
                        title: item.title,
                        icon: item.icon,
                        child: this.addChildArray(item.leaf_nodes),
                        exact: true
                    });
                }
            }
        },
        async setMenu(){
            /**
             * Function to set 'menu' array of objects for 'sidebar-menu' component.
             */

            // Make sure to whenever this function is called, the 'menu' array is empty.
            this.menu = [];
            this.addHeaderNavigation('Main Menu')
            this.addNavigation([
                // {
                //     href: '/dashboard',
                //     title: 'Dashboard',
                //     /*
                //       You can set icon as class value:
                //
                //       icon: "fa-solid fa-user",
                //
                //       Or as object with element and attributes:
                //
                //       icon: {
                //         element: 'font-awesome-icon',
                //         attributes: {
                //             icon: "fa-solid fa-user",
                //         },
                //       },
                //     */
                //     icon: {
                //         element: 'font-awesome-icon',
                //         attributes: {
                //             icon: 'fa-solid fa-user',
                //         },
                //     },
                //
                //     /* with vue-router */
                //     // external: for open the link in new tab.
                //     // external: true,
                //     /* apply active class when current route is exactly the same.
                //     (based on route records, query & hash are not relevant)*/
                //     exact: true
                // },
                {
                    href: router.resolve('/home'),
                    title: 'Home',
                    icon: {
                        element: 'font-awesome-icon',
                        attributes: {
                            icon: 'fa-solid fa-house',
                        },
                    },
                    exact: true
                },
                // {
                //     href: router.resolve('/store/deals/all?page=1'),
                //     title: 'Latest deals',
                //     icon: {
                //         element: 'font-awesome-icon',
                //         attributes: {
                //             icon: 'fa-solid fa-store',
                //         },
                //     },
                //     exact: true
                // },
            ]);
            this.addSeperator();
            this.addHeaderNavigation('Shop by Department');
            this.addDynamicImageNavigation();
            // this.addDynamicIconNavigation();

            // this.addSeperator();
            // this.addHeaderNavigation('Asking for help?');
            // this.addNavigation([
                // {
                //     href: '/contact-us/talk-to-agent',
                //     title: 'Talk to agent',
                //     icon: {
                //         element: 'font-awesome-icon',
                //         attributes: {
                //             icon: 'fa-solid fa-headset',
                //         },
                //     },
                // },
                // {
                //     href: '/contact-us',
                //     title: 'Email us',
                //     icon: {
                //         element: 'font-awesome-icon',
                //         attributes: {
                //             icon: 'fa-solid fa-envelope',
                //         },
                //     },
                //     // external: true
                // }
            // ]);
        },
        async getDataResult(endpoint) {
            /**
             * Function to get data from backend server in order to set value of 'dynamicNavArray'.
             */

            try {
                this.response = await axios.get(endpoint);
                this.dynamicNavArray = this.response.data;

                if (this.dynamicNavArray.length > 0){
                    await this.setMenu();
                }
            }
            catch (error) {
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
                setTimeout(() => {storeContentLoading.$patch({navSidebarDataLoading: false})},0);
            }
        },
    }

});

// Check if HMR is true (means in development environment), then import HMR for this store.
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useNavSidebarStore, import.meta.hot))
}