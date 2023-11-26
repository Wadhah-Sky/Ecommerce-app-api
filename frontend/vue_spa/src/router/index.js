/**
 * INFO: in this project frontend we are using static params for url query, but only the 'page' parameter
 *       is set be query string.
 *       So when you are trying to define <router-link> or make router.push() make sure to use below way:
 *
 *       {name : '<route-name>', params: { <parameter-name>: value }, query: { page: value }}
 *
 *       While if you are trying to manipulate 'page' value when define <router-link> or make router.push():
 *
 *       {path : '<route-path>', query: { page: value }}
 */

/**
 * URLs can be classified into two classes: static and dynamic.
 *
 * 1- Static URLs: do not accept string parameters and are not dynamically generated.
 *                 This means that the only way to modify the content of such a web page
 *                 is by changing the HTML code.
 *
 *                 Examples:
 *
 *                 https://www.mydomain.com/articles/my-first-article
 *                 https://www.mydomain.com/en/articles/1/my-first-article
 *
 *
 * 2- Dynamic URLs: contain a query string, which is a part of the URL that assigns values
 *                  to specified parameters. These are passed directly to the server and
 *                  used to dynamically retrieve content from a database.
 *                  Content that will be displayed on the page accordingly, which will change
 *                  based on the result of the query, without the need to touch the HTML code.
 *                  In this case, such a web page acts just like a template for the content.
 *
 *                  Examples:
 *
 *                  https://www.mydomain.com/article.php?id=1
 *                  https://www.mydomain.com/articles/page.php?article_id=1&lang=en
 *
 *
 *                  foo://example.com:8042/over/there?name=ferret#nose
 *                  \_/   \______________/\_________/ \_________/ \__/
 *                   |           |            |            |        |
 *                 scheme     authority      path       query   fragment
 */

/**
 * Important: We need to add another <router-view> inside the view component who have children
 *            routes defined in router/index.js in order to load the child components.
 */

/**
 * Info: When a user is redirected as a result of an action that occurs on a route, it is called
 *       "programmatic navigation".
 *       In Vue.js, we use router.push() method for programmatic navigation. This method pushes
 *       the new entry of the page into the history stack when the user is redirected. So that
 *       users can easily go back to the previous page by clicking the back button.
 *       This method takes three input parameters:
 *
 *       router.push(location, onComplete?, onAbort?)
 *
 *       The first one is the location that needs to be redirected, and this parameter is mandatory.
 *       The second and third parameters are optional. We can define what to be done at the end of
 *       successful navigation or in a navigation failure using them. But we don't use these two optional
 *       parameters after the Vue Router 3.1 update since router.push() method is now returning a promise
 *       after completing the navigation.
 *
 *       Examples: If we consider the location input parameter, there are multiple ways to pass it.
 *                 We can provide string paths, objects, or even named routes as the location:
 *
 *       // as a simple string
 *       router.push('messages')
 *
 *       // as an object with path
 *       router.push({ path: 'messages' })
 *
 *       // as an object with a name and params => /messages/1
 *       router.push({ name: 'messages', params: { userId: '1' } })
 *
 *       // with query string => /messages?plan=archived
 *       router.push({ path: 'messages', query: { status: 'archived' } })
 *
 * Note: "path" and "params" can’t be used at the same time. "params" will be ignored if
 *        the path is used, Therefore you need to use name instead of the path if you are
 *        passing any parameters:
 *
 *        router.push({ name: 'messages', params: { userId } }) // ->  /messages/123
 *        router.push({ path: '/messages', params: { userId } }) // ->  /messages  (This doesn't match the correct route)
 *
 * Note: Dynamic Route Matching, In web applications, it's common to see parameters passed through routes.
 *       So we need a mechanism to dynamically match those routes, and Vue-Router facilitates this feature
 *       with Dynamic segments in a route start with a colon:
 *       And when a route matches, we can access these dynamic segments through $route.params.<name_of_param>
 *       or $route.query.<name_of_query>
 *
 *       const routes = [
 *          {
 *            path: "/messages/chat/:userId",
 *            name: "Message",
 *            component: () => import("../views/Message.vue")
 *       }];
 *
 *       The same "Message" component will be loaded for each use. This is more efficient than destroying and
 *       creating a new one. But, this will prevent lifecycle hooks of that component from running even if the
 *       route is changed. So, you need to watch the $route object or use the "beforeRouteUpdate()" navigation
 *       guard to capture the changes.
 *
 * Important: query string value CAN'T be pass to the route component view as props, the only way to get their
 *            values is by using 'useRoute' method inside that component to returns current route location
 *            details like path, query or params, But, params CAN be pass as props automatically to the component
 *            view but make sure that the params names are the same when defined:
 *            1- in route{path} of your routes array.
 *            2- inside the related component view as props using defineProps().
 *
 *            And so that you don't need to access the params the way you do with query string in the component
 *            in order to get the values you need.
 *            When props is set to true, the route.params will be set as the component props.
 *
 * Info: params and query string are the same when trying to set them in the route{path}.
 */

import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

const setPageInQuery = (to) => {
  /**
   * Check before entering the component:
   * 1- if 'page' value is found in url query string, if not will set automatically as 1 into the query string.
   * 2- whether the 'page' value in url query is number or not. Not a Number, like
   *    empty value, chars or any symbol, if this case is exists then set value of 'page' parameter to be 1.
   *    isNaN() function return true if the provided value is Not a Number.
   */

  if (!to.query.page || isNaN(to.query.page) ){
    to.query.page = 1;
    return { path: to.path, query: to.query, hash: to.hash }
  }
};
const setAttributeInQuery = (to) => {
  /**
   * Check before entering the component that the current value of route.query.attr if provided
   * doesn't contain an attribute that its length bigger than 25, return only conditional attributes.
   */

  /*
    Important: in this method we don't write the code line below at the end of method:

               return { path: to.path, query: to.query, hash: to.hash }

               This because will lead to loop of redirection navigation guard, due the condition
               you wrote here that will be always true for right 'to.query.attr'.
               Delete line in else{} block, will take the effect.
   */

  if(! [null, undefined].includes(to.query.attr) ){

    // Convert attr string into array of attributes split by (,)
    const attributes = to.query.attr.split(',');

    // Initialize an empty array.
    let attrArray = [];

    for (let item of attributes){
      // Trim white spaces from start and end of the item.
      let val = item.trim();

      // In backend, we set the max length for attribute title to be 25 characters.
      if (val.length < 25){
          attrArray.push(val);
      }
    }
    // Now set 'attr' value for route query to be string of attributes seperated by comma (,).
    to.query.attr = attrArray.join();
  }
  else {
    // in case 'attr' is null or undefined.
    // Delete the 'attr' from route query if exists.
    delete to.query?.attr
  }
};
const setMinPriceInQuery = (to) => {
  /**
   * Check before entering the component:
   * 1- if 'minPrice' value is found in url query string.
   *    AND
   * 2- 'minPrice' value in url query is number or not. Not a Number, like empty value,
   *    chars, null, false or 0, if this case is exists then delete query key of 'minPrice'.
   *    OR
   * 3- 'minPrice' value in url query is negative value.
   *    OR
   * 4- 'minPrice' value in url query is bigger than 4999.
   */

  /*
    Inf0: here we need to write the code line:

          return { path: to.path, query: to.query, hash: to.hash }

          Otherwise, will not take effect.
   */

  if ((to.query.minPrice && isNaN(to.query.minPrice)) || (+to.query.minPrice < 0 || +to.query.minPrice > 4999 )) {
    delete to.query.minPrice
    return { path: to.path, query: to.query, hash: to.hash }
  }
};
const setMaxPriceInQuery = (to) => {
  /**
   * Check before entering the component:
   * 1- if 'maxPrice' value is found in url query string.
   *    AND
   * 2- 'maxPrice' value in url query is number or not. Not a Number, like empty value,
   *    chars, null, false or 0, if this case is exists then delete query key of 'maxPrice'.
   *    OR
   * 3- 'maxPrice' value in url query is less than 1.
   *    OR
   * 4- 'maxPrice' value in url query is bigger than 5000.
   */

  if ((to.query.maxPrice && isNaN(to.query.maxPrice)) || (+to.query.maxPrice < 1 || +to.query.maxPrice > 5000) ) {
    delete to.query.maxPrice
    return { path: to.path, query: to.query, hash: to.hash }
  }
};
const setSelectByInQuery = (to) => {
  /**
   * Check before entering the component that the current value of route.query.selectBy if provided
   * is one of available values.
   */

  // Available values
  const values = ['deals', 'price-low-to-high', 'price-high-to-low'];

  // Check if 'selectBy' is provided and include within available list of values, otherwise delete it.
  if(to.query.selectBy && (!values.includes(to.query.selectBy)) ) {
    delete to.query.selectBy
    return { path: to.path, query: to.query, hash: to.hash }
  }
};
// const setProductQuery = (to) => {
//   /**
//    * Check before entering the component that if both of (to.query.attr) and (to.query.itemS) is set,
//    * remove (to.query.itemS)
//    */
//
//   if( to.query.itemS && to.query.attr ) {
//     delete to.query.itemS
//     return { path: to.path, query: to.query, hash: to.hash }
//   }
// };

const removeQueryParams = (to) => {
  /**
   * Remove params from url query.
   */

  /*
  * Check whether there is any parameter in url query string by using 'length' method to find the number of params.
  * if value is NOT zero set the query as empty object.
  */
  if (Object.keys(to.query).length)
    return { path: to.path, query: {}, hash: to.hash }
};

const removeHash = (to) => {
  /**
   * Remove #value from url query.
   */

  if (to.hash) return { path: to.path, query: to.query, hash: '' }
};

// Define an array of your website URL routes.
/*
  Info: each route object in the routes' configuration is called a route record. Route records may
        be nested, Therefore when a route is matched, it can potentially match more than one route record.
        For example, the URL /posts/new will match both the parent route record (path: '/posts') and the
        child route record (path: 'new') if 'new' is a child route of 'posts' route.
*/
const routes = [
  {
    // This route is hot-loaded when the route is visited.

    /*
       optional: Specify the name view of this route that can be used to call it.
    */
    name: 'home',
    // Specify the suffix for website main url as path for this route.
    path: '/home',
    // Specify extra aliases to this path.
    alias: ['/'],
    // Specify the component/view name to be load.
    component: HomeView,
    beforeEnter: [removeQueryParams, removeHash]
  },
  {
    name: 'categoryVariation',
    path: '/categories/:slug',
    component: () => import(/* webpackChunkName: "categoryVariation" */ '../views/CategoryVariationView.vue'),
    beforeEnter: [removeHash],
    /*
      Set if this component accepts props.
      When props is set to true, the route.params will be set as the component props.
    */
    props: true
  },
  {
    /*
      Note: in this route we are using nested routes, so take in consideration:
            1- Reloading the page will always display the view or component that related to that url path.
            2- You should not name the parent route only the children, but in case there is a view or
               component related to the parent route you can name the parent.
            3- Nested paths that start with '/' will be treated as a root path. This allows you to
               leverage the component nesting without having to use a nested URL.
            4- You don't have to put '/' at the end of the parent route.
            5- If the parent route have a view or component, you can use <router-view> inside its
               view or component code to view its children components, for example 'user' view as parent
               and children could be 'about' component and 'profile' component which you can trigger
               between them using the path of each one.
    */
    path: '/store',
    /*
      Router guards on a route's configuration object those only trigger when entering the route,
      they don't trigger when the params, query or hash change e.g. going from /users/2 to
      /users/3 or going from /users/2#info to /users/2#projects. They are only triggered when
      navigating from a different route.
    */
    beforeEnter: [
        setPageInQuery,
        setAttributeInQuery,
        setMinPriceInQuery,
        setMaxPriceInQuery,
        setSelectByInQuery,
        removeHash
    ],
    /*
      meta property which accepts an object of properties and can be accessed on the route location
      and navigation guards.
    */
    // meta: { transition: 'slide-left' }
    children: [
      // {
      //   name: 'storeDeals',
      //   alias: ['/latest-deals'],
      //   path: 'deals/:categorySlug/:page?',
      //   /*
      //      route level code-splitting
      //      this generates a separate chunk (about.[hash].js) for this route
      //      which is lazy-loaded when the route is visited.
      //   */
      //   component: () => import(/* webpackChunkName: "storeDeals" */ '../views/DealsView.vue'),
      //   /*
      //      Set if this component accepts props.
      //      When props is set to true, the route.params will be set as the component props.
      //   */
      //   props: route => ({
      //     slug: route.params.categorySlug,
      //     page: route.query.page
      //   }),
      // },
      {
        name: 'storeCategory',
        path: 'category/:slug/:attr?/:minPrice?/:maxPrice?/:page?',
        /*
          route level code-splitting
          this generates a separate chunk (about.[hash].js) for this route
          which is lazy-loaded when the route is visited.
        */
        component: () => import(/* webpackChunkName: "storeCategory" */ '../views/StoreCategoryView.vue'),
        /*
           Set the parameters to be passed to component props.
        */
        props: route => ({
          slug: route.params.slug,
          attr: route.query.attr,
          minPrice: route.query.minPrice,
          maxPrice: route.query.maxPrice,
          selectBy: route.query.selectBy,
          page: route.query.page
        }),
      },
      {
        name: 'storeSearch',
        path: 'search/:query/:page?',
        component: () => import(/* webpackChunkName: "storeSearch" */ '../views/StoreSearchView.vue'),
        props: route => ({
          query: route.params.query,
          page: route.query.page
        }),
      },
    ]
  },
  {
    name: 'product',
    path: '/product/:slug/:itemS?',
    component: () => import(/* webpackChunkName: "product" */ '../views/ProductView.vue'),
    beforeEnter: [removeHash],
    /*
     Set the parameters to be passed to component props.
    */
    // Note: if you want to use 'attr':
    // 1- add method 'setProductQuery' to beforeEnter router guard.
    // 2- add 'attr' the path query parameters and set it value to related prop.
    props: route => ({
      slug: route.params.slug,
      itemS: route.query.itemS
    }),
  },
  {
    name: 'checkout',
    path: '/checkout',
    component: () => import(/* webpackChunkName: "checkout" */ '../views/CheckoutView.vue'),
    meta: { transition: 'slide-left' },
    beforeEnter: [removeQueryParams, removeHash],
    children: [
        {
          name: 'checkoutCart',
          path: 'cart',
          /*
            route level code-splitting
            this generates a separate chunk (about.[hash].js) for this route
            which is lazy-loaded when the route is visited.
          */
          component: () => import(/* webpackChunkName: "checkoutCart" */ '../views/CheckoutCartView.vue')
        },
        {
          name: 'checkoutShipping',
          path: 'shipping',
          /*
            route level code-splitting
            this generates a separate chunk (about.[hash].js) for this route
            which is lazy-loaded when the route is visited.
          */
          component: () => import(/* webpackChunkName: "checkoutShipping" */ '../views/CheckoutShippingView.vue')
        },
        {
          name: 'checkoutPayment',
          path: 'payment',
          /*
            route level code-splitting
            this generates a separate chunk (about.[hash].js) for this route
            which is lazy-loaded when the route is visited.
          */
          component: () => import(/* webpackChunkName: "checkoutPayment" */ '../views/CheckoutPaymentView.vue')
        }
    ]
  },
  {
    name: 'contact',
    path: '/contact',
    component: () => import(/* webpackChunkName: "contact" */ '../views/ContactView.vue'),
    beforeEnter: [removeQueryParams, removeHash]
  },
  {
    name: 'about',
    path: '/about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    beforeEnter: [removeQueryParams, removeHash]
  },
  {
    /* Regex to catch all paths are not define previously, this root very important:
       1- read second point of different history modes below.
       2- if not set, then <router-view> will not work.

       pathMatch: is the name of the param (represent to.path), e.g., going to /not/found yields:
                  {name: 'page-not-found', params: { pathMatch: ['not', 'found'] }}

       this is thanks to the last *, meaning repeated params, so it is
       necessary if you plan on directly navigating to the page-not-found route
       using its name, if you omit the last `*`, the `/` character in params will be
       encoded and can't accept an array of 'params' when resolving or pushing.:

       1- bad example if using named routes:
       router.resolve({ name: 'bad-not-found', params: { pathMatch: 'not/found' }}) >> '/not%2Ffound'
       2- good example:
       router.resolve({ name: 'page-not-found', params: { pathMatch: ['not', 'found'] }}) >> '/not/found'
    */
    name: "page-not-found",
    path: "/:pathMatch(.*)*",
    component: () => import(/* webpackChunkName: "not-found" */ "../views/PageNotFoundView.vue")
  }

];

const router = createRouter({

  /*
  'process.env.BASE_URL' value is the 'publicPath' value in 'vue.config.js' file.
   Note: if you set the history with it:

   history: createWebHistory()

   this will make your django project 'index.html' url print in url bar of the browser like below:

   127.0.0.1:8000/http://127.0.0.1:8080/

   The 'history' option when creating the router instance allows us to choose among different history modes.

   1- The hash history mode is created with createWebHashHistory()
      It uses a hash character (#) before the actual URL that is internally passed. Because this section of the
      URL is never sent to the server, it doesn't require any special treatment on the server level. It does however
      have a bad impact in SEO. If that's a concern for you, use the HTML5 history mode.

   2- The HTML5 mode is created with createWebHistory() and is the recommended mode.
      When using createWebHistory(), the URL will look "normal," e.g. https://example.com/user/id. Beautiful!
      Here comes a problem, though: Since our app is a single page client side app, without a proper server configuration,
      the users will get a 404 error if they access https://example.com/user/id directly in their browser. Now that's ugly.
      Not to worry: To fix the issue, all you need to do is add a simple catch-all fallback route to your server. If the
      URL doesn't match any static assets, it should serve the same index.html page that your app lives in. Beautiful,
      again!
  */
  history: createWebHistory(),
  // Specify an array of your website URL routes.
  routes
});

export default router
