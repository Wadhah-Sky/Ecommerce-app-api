<template>
  <!-- ========================= BANNER SECTION ========================= -->
  <section class="section-intro padding-y-sm">
    <div class="container">

      <div class="intro-banner-wrap">
        <agile :options="storeAgileSlider.options"
        >
          <div v-for="( banner, index ) in storeHome.dataResult.Banner" :key="index" class="slide">

            <router-link v-if="banner.frontend_path" :to="{ path: banner.frontend_path }" class="img-wrap">
              <img :src="banner.thumbnail" :alt="banner.title" >
            </router-link>
          </div>

        </agile>

      </div>

    </div> <!-- container //  -->
  </section>
  <!-- ========================= BANNER SECTION END// ========================= -->

  <!-- ========================= SWIPER SECTION  ========================= -->
  <section v-for="( slider, index ) in storeHome.dataResult.ProductGroup" :key="index"
           class="section-name padding-y-sm"
  >
    <div class="container">

      <header class="section-heading">
        <h3 class="section-title">{{slider.title}}</h3>
      </header><!-- sect-heading -->

      <div class="row">
        <div class="col-md-12">

          <swiper
              :slides-per-view=1
              :space-between=10
              :breakpoints="{
              '640': {
                slidesPerView: 1,
                spaceBetween: 15,
              },
              '768': {
                slidesPerView: 2,
                spaceBetween: 20,
              },
              '1024': {
                slidesPerView: 4,
                spaceBetween: 22,
              }}"
              :modules="modules"
              :cssMode="true"
              :navigation="true"
              :mousewheel="true"
              :keyboard="true"
              :freeMode="true"
          >

            <swiper-slide v-for="( slide, index ) in slider.products" :key="index">

              <product-card-component :product-title="slide.title"
                                      :product-slug="slide.slug"
                                      :product-item-slug="slide.product_item.slug"
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

    </div><!-- container // -->
  </section>
  <!-- ========================= SWIPER SECTION END// ========================= -->

  <!-- ========================= EXTRA SECTIONS  ========================= -->
  <section v-for="( section, index ) in storeHome.dataResult.Section"
           :key="index"
           class="section-name padding-y-sm"
  >
    <div class="container">

      <header class="section-heading">
<!--        <router-link-->
<!--            :to="-->
<!--            {-->
<!--              // name: 'categoryVariation',-->
<!--              // params: { departmentName: section.section_name }-->
<!--            }"-->
<!--            class="btn btn-outline-primary float-end">-->
<!--          See all-->
<!--        </router-link>-->
        <h3 class="section-title">{{ section.title }}</h3>
      </header><!-- sect-heading -->

      <div class="row">
        <div v-for="( card, index ) in section.cards" :key="index" class="col-md-3">

          <div v-if="card.category_slug" class="card card-product-grid" >

            <router-link
                :to="{ name: 'categoryStore', params:{ slug: card.category_slug }, query: {page: 1} }"
            >
              <img class="card-img-top img-wrap" :src="card.thumbnail" :alt="card.title">
            </router-link>

            <div class="card-body">

              <h5 class="title">{{card.title}}</h5>
              <p class="card-text"
                 style="height: 113px;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        margin-bottom: 10px;
                        text-align: justify;
                        text-justify: inter-word;"
              >
                {{card.summary}}
              </p>
              <div class="a-button-div">
                <router-link
                    :to="{ name: 'categoryStore', params:{ slug: card.category_slug }, query: {page: 1} }"
                    class="a-button"
                >
                  <span style="text-transform:none">{{card.frontend_link_text}}</span>
                </router-link>
              </div>
            </div>

          </div>

        </div> <!-- col.// -->

      </div> <!-- row.// -->


    </div><!-- container // -->
  </section>
  <!-- ========================= EXTRA SECTIONS  END// ========================= -->


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ProductCardComponent from "@/components/ProductCardComponent";
import {useHomeStore} from "@/store/Home";
import { useAgileSliderStore } from "@/store/AgileSlider";
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation, Mousewheel, Keyboard, FreeMode } from "swiper";
import {useRoute, useRouter} from "vue-router";

export default {
  name: "HomeView",
  components: {
    ProductCardComponent,
    Swiper,
    SwiperSlide
  }
}

</script>

<script setup>

/*
Note: if you are going to use props inline for <agile> component, convert props names
      from camelCase to kebab-case.
*/

/*
  Define handlers (properties, props and computed)
*/
const storeAgileSlider = useAgileSliderStore();
const storeHome = useHomeStore();
const modules = [Navigation, Mousewheel, Keyboard, FreeMode];
const router = useRouter();
const route = useRoute();

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};
const checkDataResultAvailability = async () => {
  /**
   * Check whether the retrieved data for home page sections is empty or not, if not
   * replace the current component with page-not-found component.
   */

 if (!storeHome.dataResult.Banner && !storeHome.dataResult.Section){
    /*
      In case the storeHome.getDataResult() returned a response with status code 404 or 200 (with empty result),
      we need to make sure to replace the current component before its rendered (while in setup life cycle)
      with another component (like page-not-found), be careful that you should REPLACE not PUSH to the
      'page-not-found' component because whenever you do a router.push() you add new route record into
      routing stack and if you tried to move back by pressing on back button in the browser will move
      you back to the component that you actually pushed from which will push you again to 'page-not-found'
      component again and so on while router.replace() will replace the current route record with another one.
    */
    await router.replace(
        {
          name: 'page-not-found',
          // preserve current path and remove the first char to avoid the target URL starting with `//`
          params: { pathMatch: route.path.substring(1).split('/') },
          // preserve existing query and hash if any
          query: route.query,
          hash: route.hash
        }
    );
  }

};

/*
  call functions
*/
setPageTitle("Jamie & Cassie | Home");

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
await checkDataResultAvailability();

</script>

<style lang="sass">

.agile
  &__dots
    bottom: 10px
    flex-direction: column
    right: 30px
    position: absolute

  &__dot
    margin: 5px 0

    button
      background-color: transparent
      border: 1px solid #fff
      cursor: pointer
      display: block
      height: 10px
      font-size: 0
      line-height: 0
      margin: 0
      padding: 0
      transition-duration: .3s
      width: 10px

    &--current,
    &:hover
      button
        background-color: #fff

// Slides styles
.slide
  display: block
  //height: 500px
  object-fit: cover
  width: 100%

</style>