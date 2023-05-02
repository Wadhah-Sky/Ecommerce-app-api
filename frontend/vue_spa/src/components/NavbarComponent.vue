<template>

  <header class="section-header">

    <section class="header-main border-bottom">
      <div class="container">

        <div class="row">

          <!--Logo-->
          <div class="col-3">
            <router-link :to="{name: 'home'}" class="brand-wrap">
              <img class="logo" src="../assets/images/logo/logo.png" alt="Jamie & Cassie">
            </router-link> <!-- brand-wrap.// -->
          </div>
<!--          <div class="col-2">-->
<!--            <div class="dropdown">-->
<!--              <button class="btn btn-primary dropdown-toggle"-->
<!--                      type="button"-->
<!--                      id="dropdownMenuButton1"-->
<!--                      data-bs-toggle="dropdown"-->
<!--                      aria-expanded="false"-->
<!--              >-->
<!--                <i class="fa fa-bars"></i> All category-->
<!--              </button>-->
<!--              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">-->
<!--                <li>-->
<!--                  <a class="dropdown-item" href="#">Men's Fashion </a>-->
<!--                </li>-->
<!--                <li>-->
<!--                  <a class="dropdown-item" href="#">Women's Fashion </a>-->
<!--                </li>-->
<!--                <li>-->
<!--                  <a class="dropdown-item" href="#">Kids Fashion </a>-->
<!--                </li>-->
<!--              </ul>-->
<!--            </div>  &lt;!&ndash; category-wrap.// &ndash;&gt;-->
<!--          </div> &lt;!&ndash; col.// &ndash;&gt;-->
<!--          <div class="col-2">-->
<!--            <a href="/store" class="btn btn-outline-primary">Store</a>-->
<!--          </div>-->

          <!--Search-->
          <div class="col-6">
            <form action="#" class="search">
              <div class="input-group w-10">
                <input type="text" class="form-control" style="width:60%;"
                       placeholder="Search">

                <div class="input-group-append">
                  <button class="btn btn-primary" type="submit">
                    <i class="fa fa-search"></i>
                  </button>
                </div>
              </div>
            </form> <!-- search-wrap .end// -->
          </div> <!-- col.// -->

          <!--Cart-->
          <div class="col-3">
            <div class="d-flex justify-content-end mb-3 mb-lg-0">

              <a href="#"
                 @click.capture.prevent="cartToggle"
                 class="widget-header pl-3 ml-3"
                 :style="[cartDropdown ? {color: '#ABB0BE'} : {color: '#0F1111'}]"
              >
                <div class="icon icon-sm rounded-circle border">
                  <font-awesome-icon icon="fa-solid fa-shopping-cart"/>
                </div>
                <span class="badge badge-pill notify" style="background-color: rgb(204, 12, 57);">
                  {{storeCart.itemsCount}}
                </span>
              </a>

              <template v-if="cartDropdown">

                <cart-dropdown-component :products="storeCart.products"
                                         :total-price="storeCart.totalPrice"
                                         :remove-item="storeCart.removeItem"
                />

              </template>

            </div> <!-- widgets-wrap.// -->
          </div> <!-- col.// -->

        </div> <!-- row.// -->

      </div> <!-- container.// -->
    </section> <!-- header-main .// -->

  </header> <!-- section-header.// -->

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import {useCartStore} from "@/store/Cart";
import CartDropdownComponent from "@/components/CartDropdownComponent";
import {useRoute} from "vue-router";
import {ref, watch} from 'vue';

export default {
  name: "NavbarComponent",
  components: {
    CartDropdownComponent
  }
}

</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const storeCart = useCartStore();
const route = useRoute();
const cartDropdown = ref(false);

/*
  Define functions
*/
const cartToggle = () =>{
  /**
   * Toggle the cart dropdown menu
   */

  cartDropdown.value = !cartDropdown.value;
};

// Watch route
watch(() => route, (currentValue, oldValue) =>
    {
      // When route is change, remove the cart dropdown component by set value of 'cartDropdown' to false.
      cartDropdown.value = false;
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

</style>