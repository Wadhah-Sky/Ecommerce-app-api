<template>

  <aside class="col-md-6 mb-2">

    <article class="gallery-wrap">

        <swiper :thumbs="{ swiper: thumbsSwiper }"
                :modules="modules"
                :mousewheel="true"
                :keyboard="true"
                :lazy="true"
                :slidesPerView="1"
                :spaceBetween="10"
                class="img-big-wrap"
        >

            <swiper-slide v-for="( img, index ) in props.images" :key="index">

              <!-- Required swiper-lazy class and image source specified in data-src attribute -->
              <img :src="img" :alt="`img-${index}`" class="swiper-lazy" />
              <!-- Preloader image -->
              <div class="swiper-lazy-preloader swiper-lazy-preloader-black" style="transition: all 0.3s ease-in-out">
              </div>

              <!-- Use to non-lazy -->
              <!-- <img :src="img" :alt="`img-${index}`"/> -->

            </swiper-slide> <!-- img-big-wrap.// -->

        </swiper>


        <swiper v-if="images.length > 1"
                @swiper="setThumbsSwiper"
                :cssMode="true"
                :mousewheel="true"
                :keyboard="true"
                :freeMode="true"
                :navigation="true"
                :lazy="true"
                :slidesPerView="3"
                :spaceBetween="12"
                :watchSlidesVisibility="true"
                :watchSlidesProgress="true"
                class="thumbs-wrap"
        >
          <swiper-slide v-for="( img, index ) in props.images" :key="index" class="item-thumb">

            <!-- use vue lazy loading-->
            <img v-lazy="img" :alt="`img-${index}`" />

            <!-- Use to non-lazy -->
            <!-- <img :src="img" :alt="`img-${index}`"/> -->

          </swiper-slide>

        </swiper>

    </article> <!-- gallery-wrap .end// -->

  </aside>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import { Swiper, SwiperSlide } from 'swiper/vue';
import SwiperCore, { Navigation, Mousewheel, Keyboard, FreeMode, Thumbs } from "swiper";
import{ ref, defineProps } from "vue";

export default {
  name: "ProductItemGalleryComponent",
  components: {
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
  images: {
    type: Array,
    required: true
  }
});
// const storeProduct = toRef(props, 'storeProduct');
const modules = [Mousewheel, Keyboard];
const thumbsSwiper = ref(null);

// install Swiper modules
SwiperCore.use([Thumbs, Navigation, Mousewheel, Keyboard, FreeMode]);

/*
  Define functions
*/
const setThumbsSwiper = (swiper) => {
  /**
   * Method to change thumbSwiper value when @swiper emit.
   *
   * Note: thumbSwiper is connected in two ways with props.thumbs of 'img-big-wrap' swiper.
   */
  thumbsSwiper.value = swiper;
};

</script>

<style scoped>

.swiper-slide {
  background-size: cover;
  background: center #fff;
  text-align: center;
  font-size: 18px;

  /* Center slide text vertically */
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  -webkit-justify-content: center;
  justify-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  -webkit-align-items: center;
  align-items: center;
}

.thumbs-wrap .swiper-slide {
  opacity: 0.4;
}

.thumbs-wrap .swiper-slide-thumb-active {
  opacity: 1;
  cursor: default!important;
}

</style>