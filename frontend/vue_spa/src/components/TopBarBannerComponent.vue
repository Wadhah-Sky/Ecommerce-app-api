<template>

  <div class="row" id="top-block">
    <div class="col-12">

      <swiper :slides-per-view=1
              :space-between=0
              :centeredSlides="true"
              :loop="true"
              :modules="modules"
              :autoplay="{
                delay: 4000,
                disableOnInteraction: false,
              }"
              :cssMode="true"
              :mousewheel="true"
              :keyboard="true"
      >

        <swiper-slide v-for="(banner, index) in props.data" :key="index">

          <div>
            <span>{{banner.summary}}</span>

            <template v-if="!['', null, undefined].includes(banner.url)">

              <a id="banner-link"
                 :href="banner.url"
                 :target="banner.url_target"
              >
                {{banner.frontend_link_text}}
              </a>

            </template>

          </div>

        </swiper-slide>

      </swiper>
    </div>

  </div> <!-- row.// -->

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, Mousewheel, Keyboard } from "swiper/modules";
import { defineProps } from 'vue';

export default {
  name: "TopBarBannerComponent",
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
  data: {
    type: Array,
    required: true
  }
})
const modules = [Autoplay, Mousewheel, Keyboard];

</script>

<style scoped>

#top-block{
  position:relative;
  min-height: 20px;
  display: block;
  margin: 0 auto;
  align-content: center;
  text-align: center;
  padding: 3px 0;
  color: #fff;
  font-size: 15px;
  /*opacity: 0.5;*/ /* opacity will cause to cut of slider when element overlay it*/
  z-index: 1;
  word-spacing: 1px;
  background: linear-gradient(90deg, #fff 0%, #0f1111 20%, #0f1111 80%, #fff 100%);
  background: -webkit-linear-gradient(90deg, #fff 0%, #0f1111 20%, #0f1111 80%, #fff 100%);
  background: -moz-linear-gradient(90deg, #fff 0%, #0f1111 20%, #0f1111 80%, #fff 100%);
  background: -ms-linear-gradient(90deg, #fff 0%, #0f1111 20%, #0f1111 80%, #fff 100%);
}

#banner-link{
  margin-left: 5px;
  color: #fff;
}

#banner-link:hover{
  color: #FCE205; /*yellow*/
  /*color: #fccb06; golden yellow*/
  transition: all 0.2s ease-in-out;
}

.swiper-slide{
  padding-left: 11%;
  padding-right: 11%;
}

@media only screen and (max-width:700px){
  #top-block{
    font-size: 14px;
  }
}
</style>