<template>

  <div class="container">

    <div class="card shopping-cart">

      <div class="shopping-cart-header">

        <div class="shopping-cart-total">
          <span class="lighter-text me-1">Total:</span>
          <span class="main-color-text">{{props.totalPrice}}</span>
        </div>

      </div> <!--end shopping-cart-header -->

      <div class="scroll-menu">

          <ul class="shopping-cart-items">

            <template v-if="props.products.length > 0">

              <li v-for="(item, index) in props.products" :key="index"
                  class="clearfix">

                <div class="row ms-1 me-1 ps-0 pe-0 ">

                  <!--This to be consider the frame of image-->
                  <div class="col-3 me-1 pt-2 pb-2"
                       style="vertical-align: middle; padding: 0; width: 55px; height: 70px;"
                  >
                    <router-link :to="{name: 'product', params: { slug: item.slug }, query: { itemS: item.itemS }}"
                                 style="text-decoration: none"
                    >

                      <img v-lazy="item.thumbnail" :alt="item.title">

                    </router-link>

                  </div>

                  <div class="col-8 ms-1 ps-0 pe-0">

                    <router-link :to="{name: 'product', params: { slug: item.slug }, query: { itemS: item.itemS }}"
                                 class="item-name"
                    >
                      {{ item.title }}
                    </router-link>

                    <div class="row row-cols-auto">

                      <template v-for="(val, index) in item.attributes"
                                :key="index"
                      >

                        <span class="col-4 pe-0" style="display: inherit; font-size: 12px; font-weight: 400;">{{index}}</span>
                        <span class="col-8 ps-1 pe-0 align-self-center" style="font-size: 12px;">{{ val }}</span>

                      </template>

                    </div>

                    <span class="item-price">{{item.currencySymbol }}{{ item.price }}</span>
                    <span class="remove-item" @click="props.removeItem(index)">Remove</span>

                    <!-- <span class="item-quantity">Quantity: </span>-->

                  </div>
                </div>

              </li>
            </template>

            <li v-else>
              <div class="row ms-0 me-0 pt-2 text-center clearfix">
                <div class="col align-self-center">Cart is empty</div>
              </div>
            </li>


          </ul>

      </div>

      <a v-if="props.products.length > 0" href="#" class="button">Checkout</a>

    </div> <!--end shopping-cart -->

  </div> <!--end container -->

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import{defineProps} from "vue";

export default {
  name: "CartDropdownComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  products: {
    type: Array,
    required: true
  },
  totalPrice: {
    type: [Number, String],
    required: true
  },
  removeItem: {
    type: Function,
    required: true
  }
});

/*
  Define functions
*/

</script>

<style scoped lang="scss">

$main-color: #0F1111;
$light-text: #ABB0BE;

*, *:before, *:after {
  box-sizing: border-box;
}

.lighter-text {
  color: $light-text;
}

.main-color-text {
  color: $main-color;
}

.container {
  position: absolute!important;
  margin-top: 78px;
  margin-right: -20px;
  width: 300px;
  z-index: 88!important;
}

.shopping-cart {
  float: right;
  background: white;
  width: 280px;
  position: relative;
  border-radius: 3px;
  padding: 20px;
  transition: all 1.9s ease-in-out;
  -webkit-transition: all 1.9s ease-in-out;


  .shopping-cart-header {
    border-bottom: 1px solid #E8E8E8;
    padding-bottom: 15px;

    .shopping-cart-total {
      float: right;
    }
  }

  .shopping-cart-items {
    list-style: none;
    padding-top: 8px;
    padding-left: 0;

    li {
      margin-bottom: 12px;
    }

    // if you dont use 'max' with height and width, the image will show as resized (fill).
    // use transform 'scale' to show image in good shape.
    img {
      vertical-align: middle;
      overflow-clip-margin: inherit;
      overflow: clip;
      //transform: scale(0.8);
      max-width: 100%;
      max-height: 100%;
    }

    .item-name {
      color: $main-color;
      text-decoration: none;
      display: block;
      padding-top: 0;
      font-size: 14px;

      text-overflow: ellipsis;
      overflow: hidden;
      display: -webkit-box !important;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      white-space: normal;
    }
    .item-name:hover{
      text-decoration: underline;
    }

    .item-price {
      color: #B12704;
      font-size: 14px;
      font-weight: 400;
    }

    .remove-item {
      cursor: pointer;
      float: right;
      color: rgb(204, 12, 57);
      font-size: 13px;
    }
    .remove-item:hover{
      color: $light-text;
    }

    .item-quantity {
      color: $light-text;
      font-size: 13px;
    }
  }

}

.scroll-menu{
  min-height: 10vh;
  max-height: 35vh;
  overflow-y: auto;
  margin: 5px 0 0 0;
  padding: 0;
}

::-webkit-scrollbar {
  width: 3px;
  border-radius: 4px;
  z-index: 99;
  opacity: 0;
  transition: 0.3s opacity ease;
}

/* Track */
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px #fff;
    -webkit-border-radius: 4px;
    border-radius: 4px;
    cursor: pointer;

}

/* Handle */
::-webkit-scrollbar-thumb {
  -webkit-border-radius: 4px;
  border-radius: 4px;
  background: #aaa;
  -webkit-box-shadow: inset 0 0 6px #fff;
  transform: translate(0%);
  display: block;
  opacity: 1;
  cursor: pointer;
  user-select: none;
  transition: 0.3s opacity ease;
}

ul.scrollmenu {
  overflow: auto;
  white-space: nowrap;
}

ul.scrollmenu::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
}

ul.scrollmenu{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.shopping-cart:after {
	bottom: 100%;
	left: 89%;
  content: " ";
	height: 0;
	width: 0;
	position: absolute;
	pointer-events: none;
  border: 8px solid transparent;
  border-bottom-color: $main-color;
  margin-left: -8px;
}

.button {
  background: $main-color;
  color:white;
  text-align: center;
  padding: 12px;
  text-decoration: none;
  display: block;
  border-radius: 3px;
  font-size: 16px;
  margin: 25px 0 15px 0;

  &:hover {
   // background: lighten($main-color, 3%);
    background: #e9ecef;
    color: #0f1111;
    transition: color 200ms ease-in-out;
  }
  &:active{
    transform: translateY(3%);
    transition: transform 0.2s;
  }
}

.clearfix:after {
  content: "";
  display: table;
  clear: both;
}

</style>