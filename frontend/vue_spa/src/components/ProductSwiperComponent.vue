<template>

  <!-- ========================= SWIPER SECTION  ========================= -->

      <header class="section-heading">
        <h3 class="section-title">{{props.sliderTitle}}</h3>
      </header><!-- sect-heading -->

      <div class="row">
        <div class="col-md-12">

          <swiper
              :slides-per-view=1
              :space-between=10
              :breakpoints="{
              '330': {
                slidesPerView: 2,
                spaceBetween: 15,
              },
              '768': {
                slidesPerView: 3,
                spaceBetween: 20,
              },
              '1024': {
                slidesPerView: 4,
                spaceBetween: 22,
              }}"
              :modules="modules"
              :cssMode="true"
              :navigation="!props.autoplay"
              :mousewheel="true"
              :keyboard="true"
              :freeMode="true"
              :lazy="true"
              :autoplay="{
                delay: 3000,
                disableOnInteraction: true,
              }"
              :loop="props.autoplay"
          >

            <swiper-slide v-for="( slide, index ) in props.products" :key="index">

              <product-card-component :product-title="slide.title"
                                      :slug="slide.slug"
                                      :item-s="slide.product_item.slug"
                                      :attr="slide.product_item.attributes.join()"
                                      :thumbnail="slide.product_item.thumbnail"
                                      :price-currency-symbol="slide.product_item.price_currency_symbol"
                                      :list-price-amount="slide.product_item.list_price_amount"
                                      :deal-price-amount="slide.product_item.deal_price_amount"
                                      :promotion-title="slide.product_item.promotion_title"
                                      :promotion-summary="slide.product_item.promotion_summary"
              />

            </swiper-slide>

          </swiper>
        </div>

      </div> <!-- row.// -->

  <!-- ========================= SWIPER SECTION END// ========================= -->

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ProductCardComponent from "@/components/ProductCardComponent";
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, Navigation, Mousewheel, Keyboard, FreeMode } from "swiper/modules";
import { defineProps} from "vue";

export default {
  name: "ProductSwiperComponent",
  components: {
    ProductCardComponent,
    Swiper,
    SwiperSlide
  }
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
  sliderTitle: {
    type: String,
    required: true
  },
  autoplay: {
    type: Boolean,
    default: false
  }
});
const modules = [Mousewheel, Keyboard, FreeMode];

if (props.autoplay === true){
  modules.push(Autoplay);
}
else {
  modules.push(Navigation)
}

</script>

<style scoped>

@media (min-width: 280px) and (max-width: 767px) {
  .section-title{
    font-size: 17px;
  }
}

</style>