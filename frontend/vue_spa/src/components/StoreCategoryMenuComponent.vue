<template>

  <header>
    <div class="scroll-menu">

          <router-link
              :to="{
                     name: route.name,
                     params: { slug: props.slug },
                     query: {
                       minPrice: route.query.minPrice,
                       maxPrice: route.query.maxPrice,
                       selectBy: route.query.selectBy,
                       page: 1
                     }
                  }"
              v-slot="{ href, navigate, isActive, isExactActive }"
              custom
          >
            <a :href="href"
               :class="[isActive ? 'router-link-active' : '', isExactActive ? 'router-link-exact-active' : '']"
               @click="navigate"
               :style="[ isActive ? { pointerEvents: 'none', display: 'inline-block' } : '']"

            >

              <label class="check-label"
                     :tabindex="href === route.fullPath ? -1 : 0">

                <input type="checkbox"
                       class="check-input"
                       :checked="isActive"
                       :disabled="isActive"
                       value="All"/>

                <span class="btn btn-white-dark">All</span>

              </label>
            </a>

          </router-link>

        <template v-if="props.data.length > 1">

            <router-link
                v-for="( item, index ) in props.data" :key="index"
                :to="{
                     name: route.name,
                     params: { slug: item.slug},
                     query: {
                       minPrice: route.query.minPrice,
                       maxPrice: route.query.maxPrice,
                       selectBy: route.query.selectBy,
                       page: 1
                     }
                  }"
                v-slot="{ href, navigate, isActive, isExactActive }"
                custom
            >
              <a :href="href"
                 :class="[isActive ? 'router-link-active' : '', isExactActive ? 'router-link-exact-active' : '']"
                 @click="navigate"
                 :style="[ isActive ? { pointerEvents: 'none', display: 'inline-block' } : '']"

              >

                <label class="check-label"
                       :tabindex="href === route.fullPath ? -1 : 0">

                  <input type="checkbox"
                         class="check-input"
                         :checked="isActive"
                         :disabled="isActive"
                         :value="item.title"
                  />

                  <span class="btn btn-white-dark">{{ item.title }}</span>

                </label>
              </a>

            </router-link>

        </template>

    </div>
  </header>
  <!-- ========================= SECTION CONTENT Without Swiper ========================= -->
<!--  <header>-->

<!--    <div class="menu-group" >-->

<!--      <div class="row mb-3" >-->

<!--          <div class="row row-cols-auto" >-->

<!--            <div class="col" >-->

<!--              <router-link-->
<!--                  :to="{-->
<!--                     name: 'categoryStore',-->
<!--                     params: { ...route.params, slug: props.slug },-->
<!--                     query: { ...route.query, page: 1 }-->
<!--                  }"-->
<!--                  v-slot="{ href, isExactActive }"-->
<!--              >-->

<!--                <label class="check-label" :tabindex="href === route.fullPath ? -1 : 0">-->

<!--                  <input type="checkbox"-->
<!--                         class="check-input"-->
<!--                         :checked="isExactActive"-->
<!--                         :disabled="href === route.fullPath"-->
<!--                         value="All">-->

<!--                  <span class="btn btn-white-dark"> All </span>-->

<!--                </label>-->

<!--              </router-link>-->

<!--            </div>-->

<!--            <template v-if="props.data.length > 1">-->
<!--              <div v-for="( item, index ) in props.data" :key="index" class="col">-->

<!--                <router-link-->
<!--                    :to="{-->
<!--                     name: 'categoryStore',-->
<!--                     params: { ...route.params, slug: item.slug},-->
<!--                     query: { ...route.query, page: 1 }-->
<!--                  }"-->
<!--                    v-slot="{ href, isExactActive }"-->
<!--                >-->

<!--                  <label class="check-label" :tabindex="href === route.fullPath ? -1 : 0">-->

<!--                    <input type="checkbox"-->
<!--                           class="check-input"-->
<!--                           :checked="isExactActive"-->
<!--                           :disabled="href === route.fullPath"-->
<!--                           :value="item.title"-->
<!--                    >-->

<!--                    <span class="btn btn-white-dark active"> {{ item.title }} </span>-->

<!--                  </label>-->

<!--                </router-link>-->

<!--              </div>-->
<!--            </template>-->

<!--          </div>-->

<!--      </div>-->

<!--    </div>-->

<!--  </header>-->


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {useRoute} from "vue-router";
import {defineProps} from "vue";

export default {
  name: "StoreCategoryMenuComponent",
  components:{
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
  },
  slug: {
    type: String,
    required: true
  }
});
const route = useRoute();

/*
  Define functions
*/

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/

</script>

<style scoped>

div.scroll-menu {
  overflow: auto;
  white-space: nowrap;
}

div.scroll-menu::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
}

div.scroll-menu{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

div.scroll-menu a {
  display: inline-block;
  margin-right: 11px;
}

/*.menu-group .row .col{*/
/*  padding-right: 0px;*/
/*  padding-left: 11px;*/
/*  padding-top: 12px;*/
/*}*/

</style>