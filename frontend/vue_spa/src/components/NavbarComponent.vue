<template>

  <header class="section-header">

    <section class="border-bottom">
      <div class="container">

        <template v-if="storeHome.dataResult.TopBanner.length > 0">
          <top-bar-banner-component :data="storeHome.dataResult.TopBanner" />
        </template>

        <nav class="row">

          <div id="nav-icon"
               class="col-2 me-0"
               :class="[props.showNavSidebar ? 'open' : '']"
               @click="props.toggleNavSidebarView"
          >
            <span></span>
            <span></span>
            <span></span>
          </div>

          <!--<div class="menu-icon"></div>-->

          <div class="col-8 justify-content-center logo"
               style="max-width: 250px; max-height: 60px; vertical-align: middle; padding: 0;"
          >

            <router-link :to="{name: 'home'}" style="position: absolute; width: 235px; height: 60px;" />

            <img src="../assets/images/logo/Jamie-and-Cassie-logo.svg"
                 width="280"
                 height="60"
                 id="logo-img"
                 alt="Jamie & Cassie icon"
                 role="img"
              />

          </div>

          <div class="col-2 d-flex justify-content-end mb-lg-0" style="position: relative">

            <!-- search part-->
            <div ref="searchBtn" class="search-icon">
              <font-awesome-icon icon="fa-solid fa-magnifying-glass"/>
            </div>

            <div ref="cancelBtn" class="cancel-icon">
              <font-awesome-icon icon="fa-solid fa-xmark"/>
            </div>

            <form ref="searchForm" class="justify-content-end" @submit.prevent>
              <input v-model="searchVal" type="search" class="search-data" placeholder="Search" required>
              <button type="submit" @click="submitSearch">
                <font-awesome-icon icon="fa-solid fa-magnifying-glass"/>
              </button>
            </form>

            <!-- end search part-->

            <!-- cart part-->
            <a href="#"
               @click.capture.prevent="toggleCartMenu"
               id="shopping-cart-dropdown-link"
               class="widget-header"
               :style="[showCartDropDownMenu ? {color: '#ABB0BE'} : {color: '#0F1111'}]"
            >
              <div class="icon icon-sm rounded-circle border">
                <font-awesome-icon icon="fa-solid fa-shopping-cart"/>
              </div>
              <span v-show="storeCheckout.itemsCount > 0"
                    class="badge badge-pill notify"
                    style="background-color: rgb(204, 12, 57);"
              >
                {{ storeCheckout.itemsCount }}
              </span>
            </a>

            <template v-if="showCartDropDownMenu">

              <cart-dropdown-component :products="storeCheckout.cartProducts"
                                       :cart-total-price-amount="storeCheckout.cartTotalPriceAmount"
                                       :cart-price-currency-symbol="storeCheckout.cartApiPriceCurrencySymbol"
                                       :remove-item="storeCheckout.removeItem"
              />

            </template>

            <!-- end cart part-->

          </div> <!-- widgets-wrap.// -->

        </nav>


      </div> <!-- container.// -->
    </section> <!-- header-main .// -->

  </header> <!-- section-header.// -->

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import CartDropdownComponent from "@/components/CartDropdownComponent";
import TopBarBannerComponent from "@/components/TopBarBannerComponent";
import {useRoute, useRouter} from "vue-router";
import {defineProps, ref, toRef, watch, onBeforeMount, onMounted, onUnmounted} from 'vue';

export default {
  name: "NavbarComponent",
  components: {
    CartDropdownComponent,
    TopBarBannerComponent
  }
}

</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storeHome: {
    type: Object,
    required: true
  },
  storeCheckout: {
    type: Object,
    required: true
  },
  showCartDropDownMenu: {
    type: Boolean,
    default: false
  },
  showNavSidebar: {
    type: Boolean,
    default: false
  },
  toggleNavSidebarView: {
    type: Function
  }
});
const storeHome = toRef(props, 'storeHome');
const storeCheckout = toRef(props, 'storeCheckout');
const route = useRoute();
const router = useRouter();
const showCartDropDownMenu = ref(props.showCartDropDownMenu);
const searchBtn = ref(null);
const cancelBtn = ref(null);
const searchForm = ref(null);
const searchVal = ref(null);

/*
  Define functions
*/
const handleClick = (e) => {
  /**
   * Method to handle click event
   */

  /*
       We use The closest() method of the Element interface traverses the element (that
       trigger the event) and its parents (heading toward the document root) until it finds
       a node that matches the specified CSS selector.
     */

  if(e.target.closest(".cancel-icon")){
    searchBtn.value.classList.remove("hide");
    cancelBtn.value.classList.remove("show");
    searchForm.value.classList.remove("active");
    cancelBtn.value.style.color = "#ABB0BE";
  }
  if(e.target.closest(".search-icon")){
    searchForm.value.classList.add("active");
    searchBtn.value.classList.add("hide");
    cancelBtn.value.classList.add("show");
  }
  if(e.target.closest("#shopping-cart-dropdown-link, #shopping-cart")){
    /*
       Pass if clicked element:
       1- '.cart-dropdown-menu-link'.
       2- '.shopping-cart' (the container of cart dropdown menu)
    */
    return false;
  }
  else if (showCartDropDownMenu.value) {
    showCartDropDownMenu.value = false;
    //storeCheckout.value.$patch({showCartDropDownMenu: false});
  }
};
const toggleCartMenu = () =>{
  /**
   * Toggle the cart dropdown menu
   */

  showCartDropDownMenu.value = !showCartDropDownMenu.value;
};
const submitSearch = () => {
  /**
   * Submit the search value
   */

  if (!['', 0, null].includes(searchVal.value)) {
    // push new router state.
    router.push({
      name: 'storeSearch',
      params: {query: searchVal.value},
      query: {page: 1}
    });
  }
};

// Life-cycle
onBeforeMount(() => {
  // Check that if current route name is 'storeSearch' (means search view) and query parameter
  // is not empty/null or 0
  if(router.currentRoute.value.name === 'storeSearch' && !['', 0, null].includes(route.params.query)){
    // Check that current value of 'searchVal' is not null
    if(searchVal.value === null){
      // Then set the value of query parameter to 'searchVal'.
      searchVal.value = route.params.query;
    }
  }
});
onMounted(() => {

  /*
    We need to listen to click event whenever happens on website 'document' with exception
    to certain element, in order to close the cart dropdown menu component if it opens.
    So need to set a handler on 'document' that listen for event click whenever triggered.
   */
  document.addEventListener("click", e => handleClick(e));

});
onUnmounted(() => {
  document.removeEventListener("click", e => handleClick(e))
});

// Watch route
watch(() => route, (currentValue, oldValue) =>
    {
      // When route is change, remove the cart dropdown component by set value of 'showCartDropDownMenu' to false.
      showCartDropDownMenu.value = false;
      storeCheckout.value.$patch({showCartDropDownMenu: false});
    },
    {
      deep: true
    }
);

</script>

<style scoped lang="scss">

$main-color: #0F1111;
$light-text: #ABB0BE;

.icon{
  transition: color 200ms ease-in-out;
}

.icon:hover{
  color: $light-text!important;
}
/////////////////////////////////////

nav{
  background: #fff;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  padding-top: 5px;
  margin-bottom: 5px;
}

nav #logo-img {
  width: 280px;
  height: 60px;
  vertical-align: middle;
  padding-bottom: 13px;
  margin-left: -15px;
  object-fit: fill
}

nav form{
  display: flex;
  position: absolute;
  height: 40px;
  padding: 2px;
  margin-left: 0;
  margin-right: 90px;
  margin-top: 5px;
  background: #fff;
  min-width: 280px;
  max-width: 280px;
  border-radius: 2px;
  border: 1px solid rgba(155,155,155,0.2);
  z-index: 30;
}
nav form .search-data{
  width: 100%;
  height: 100%;
  padding: 0 10px;
  color: $main-color;
  font-size: 15px;
  border: none;
  font-weight: 500;
  background: #fff;
}
nav form button{
  padding: 0 15px;
  color: $main-color;
  font-size: 17px;
  background: #fff;
  border: none;
  border-radius: 2px;
  cursor: pointer;
}

nav form .search-data:focus{
  outline: none
}

nav .cancel-icon,
nav .search-icon{
  position: absolute;
  width: 40px;
  text-align: center;
  padding: 10px;
  font-size: 18px;
  margin-right: 48px;
  color: $main-color;
  cursor: pointer;
  display: none;
}

nav form button:hover,
nav .fa-magnifying-glass:hover{
  color: $light-text;
  transition: color 200ms ease-in-out;
}

nav .fa-xmark:hover{
  color: rgb(204, 12, 57);
  transition: color 200ms ease-in-out;
}

.content{
  position: absolute;
  top: 50%;
  left: 50%;
  text-align: center;
  transform: translate(-50%, -50%);
}
.content header{
  font-size: 30px;
  font-weight: 700;
}
.content .text{
  font-size: 30px;
  font-weight: 700;
}
.space{
  margin: 10px 0;
}

.content{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.content header{
  font-size: 30px;
  font-weight: 700;
}
.content .text{
  font-size: 30px;
  font-weight: 700;
}
.content .space{
  margin: 10px 0;
}

/////////////////////////////////////

#nav-icon{
  width: 20px;
  height: 30px;
  position: relative;
  margin: 20px 3px 0 0;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
  -webkit-transition: .5s ease-in-out;
  -moz-transition: .5s ease-in-out;
  -o-transition: .5s ease-in-out;
  transition: .5s ease-in-out;
  cursor: pointer;
  z-index: 1;
}

#nav-icon span {
  display: block;
  position: absolute;
  height: 2px;
  width: 85%;
  background: #0F1111;
  font-size: 10px;
  border-radius: 9px;
  opacity: 1;
  left: 0;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
  -webkit-transition: .25s ease-in-out;
  -moz-transition: .25s ease-in-out;
  -o-transition: .25s ease-in-out;
  transition: .25s ease-in-out;
}

#nav-icon:hover > span{
  background: $light-text!important;
}

#nav-icon span:nth-child(1) {
  top: 0px;
}

#nav-icon span:nth-child(2) {
  top: 9px;
}

#nav-icon span:nth-child(3) {
  top: 18px;
}

#nav-icon.open span:nth-child(1) {
  top: 10px;
  -webkit-transform: rotate(135deg);
  -moz-transform: rotate(135deg);
  -o-transform: rotate(135deg);
  transform: rotate(135deg);
}

#nav-icon.open span:nth-child(2) {
  opacity: 0;
  left: -60px;
}

#nav-icon.open span:nth-child(3) {
  top: 10px;
  -webkit-transform: rotate(-135deg);
  -moz-transform: rotate(-135deg);
  -o-transform: rotate(-135deg);
  transform: rotate(-135deg);
}

@media only screen and (max-width: 349px) {
  nav .logo{
    width: 150px!important;
    margin-left: -30px!important;
    padding-left: 3px!important;
  }
  nav .logo > a{
    max-width: 140px;
  }
  nav .logo > img{
    width: 170px!important;
  }
  nav .search-icon,
  nav .cancel-icon{
    font-size: 17px;
    margin-right: 35px;
  }
  nav form{
    margin-right: 46px!important;
  }
  nav .icon-sm{
    padding: 0;
    font-size: 17px;
    width: 38px;
  }
  nav .notify{
    font-size: 9px;
  }

  #nav-icon span:nth-child(1) {
    top: -3px;
  }

  #nav-icon span:nth-child(2) {
    top: 4px;
  }

  #nav-icon span:nth-child(3) {
    top: 11px;
  }
}

@media only screen and (min-width: 350px) and (max-width: 700px) {
  nav .logo{
    width: 210px;
    margin-left: -63px;
  }
  nav .logo > a{
    max-width: 240px;
  }
  nav .log > img{
    width: 250px;
  }
  nav .search-icon,
  nav .cancel-icon{
    margin-top: 4px;
    font-size: 17px;
  }
  nav form{
    margin-right: 58px!important;
  }
  nav .icon-sm{
    font-size: 17px;
  }
  nav .notify{
    font-size: 10px;
  }
}

@media (max-width: 1245px) {
  nav{
    padding: 0 50px;
  }
}
@media (max-width: 1140px){
  nav{
    padding: 0px;
  }
  nav form{
    min-width: 180px;
    max-width: 200px;
    top: 80px;
    margin-right: 60px;
    opacity: 0;
    pointer-events: none;
    transition: top 0.3s ease, opacity 0.1s ease;
  }
  nav form.active{
    top: 95px;
    opacity: 1;
    pointer-events: auto;
  }
  nav form:before{
    position: absolute;
    content: " ";
    top: -6px;
    right: 0;
    width: 0;
    height: 0;
    z-index: -1;
    border: 8px solid transparent;
    border-bottom-color: $main-color;
    margin: -20px 0 0;
  }
  nav form:after{
    position: absolute;
    content: '';
    height: 60px;
    padding: 2px;
    background: #fff;
    border-radius: 2px;
    border: 1px solid rgba(155,155,155,0.2);
    min-width: calc(100% + 20px);
    z-index: -2;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
  nav form .search-data{
    font-size: 12px!important;
  }
  nav .menu-icon{
    display: block;
  }
  nav .search-icon,
  nav .menu-icon span{
    display: block;
  }
  nav .menu-icon span.hide,
  nav .search-icon.hide{
    display: none;
  }
  nav .cancel-icon.show{
    display: block;
  }
}

@media only screen and (min-width: 700px) {
  #nav-icon{
    display: none!important;
  }
}

</style>