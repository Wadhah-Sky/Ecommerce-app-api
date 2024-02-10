<template>
  <!-- ========================= BANNER SECTION ========================= -->
  <section class="section-intro padding-y-sm bg-white">
    <div class="container">

      <div class="intro-banner-wrap">
        <agile v-if="storeHome.dataResult.Banner && storeHome.dataResult.Banner.length > 0"
               :options="storeAgileSlider.options"
        >
          <div v-for="( banner, index ) in storeHome.dataResult.Banner" :key="index" class="slide">

            <a v-if="banner.frontend_path" :href="banner.frontend_path" class="img-wrap" style="max-width: 1118px; max-height: 300px;">
              <img v-lazy="banner.thumbnail" :alt="banner.title" width="1118" height="300">
            </a>
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

      <product-swiper-component :slider-title="slider.title" :products="slider.products" :autoplay="slider.frontend_autoplay" />

    </div>

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

      <div class="row section-cards">
        <div v-for="( card, index ) in section.cards" :key="index" class="col-sm-6 col-md-6 col-lg-3 col-xxl-2">

          <div v-if="card.category_slug" class="card card-product-grid" >

            <router-link
                :to="{ name: 'storeCategory', params:{ slug: card.category_slug }, query: {page: 1} }"
            >
              <img v-lazy="card.thumbnail" :alt="card.title" class="img-wrap card-img-top" width="260" height="220" style="object-fit: contain; -o-object-fit: contain">
            </router-link>

            <div class="card-body">

              <h5 class="title" style="text-align: center">{{card.title}}</h5>
              <p class="card-text" style="text-align: center">
                {{card.summary}}
              </p>
              <div class="a-button-div" style="margin-top: 10px">
                <router-link
                    :to="{ name: 'storeCategory', params:{ slug: card.category_slug }, query: {page: 1} }"
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
import {useHomeStore} from "@/store/Home";
import { useAgileSliderStore } from "@/store/AgileSlider";
import ProductSwiperComponent from "@/components/ProductSwiperComponent";
import {useRoute, useRouter} from "vue-router";

export default {
  name: "HomeView",
  components: {
    ProductSwiperComponent
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
const router = useRouter();
const route = useRoute();
const storeHome = useHomeStore();
const storeAgileSlider = useAgileSliderStore();

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

  // Check if 'Banner' and 'Section' is exists.
  if (storeHome.dataResult.Banner && storeHome.dataResult.Section) {

    if (storeHome.dataResult.Banner.length === 0 && storeHome.dataResult.Section.length === 0) {
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
            params: {pathMatch: route.path.substring(1).split('/')},
            // preserve existing query and hash if any
            query: route.query,
            hash: route.hash
          }
      );
    }

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
  height: 300px
  width: 100%

.slide img
  object-fit: fill
  -o-object-fit: fill

p .card-text
  position: absolute
  height: 113px
  overflow: hidden
  text-overflow: ellipsis
  margin-bottom: 10px
  //text-align: justify
  text-justify: inter-word

.section-cards .card-product-grid
  min-height: 370px

</style>

<style lang="scss">

@media (min-width: 280px) and (max-width: 767px) {
  // .agile__slides > img
  .slide {
    height: 170px !important;
    width: 100% !important;
  }

  .slide img {
    height: 170px;
    width: 100%;
    object-fit: fill;
    -o-object-fit: fill;
  }

}

</style>

<style lang="scss" scoped>

// override the default min-width value (576px) of .col-sm-* column to be 330px
// also you should set the of max-width to same column as breakpoint to .col-md-* which by default it's 768px
@media (min-width: 280px) and (max-width: 767px) {
  .col-sm-6 {
    flex: 0 0 auto;
    width: 50%;
  }
  .section-title{
    font-size: 17px;
  }
  .section-cards .card-img-top{
    height: 200px;
  }
  .section-cards .card-body{
    padding: 3px 6px;
  }
  .section-cards .title{
    font-size: 14px;
  }
  .section-cards .card-text{
    font-size: 13px;
  }
}

</style>