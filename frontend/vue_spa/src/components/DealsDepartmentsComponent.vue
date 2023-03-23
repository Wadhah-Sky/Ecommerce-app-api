<template>

    <header>

    <div class="types-group">

      <div class="row mb-3">

        <div class="row mb-3">

          <div class="row">

            <div class="section-title link-title">

              <h4>

                <component
                    :is="props.data.length <= 1 ? 'span': 'router-link'"
                    :to="{
                     name: 'dealsStore',
                     params: { ...route.params, slug: 'all' },
                     query: { ...route.query, page: 1 }
                    }"
                >
                  <span> Latest deals </span>
                </component>

              </h4>

            </div>

          </div>

          <div class="row row-cols-auto">

            <div class="col" >

              <router-link
                  :to="{
                     name: 'dealsStore',
                     params: { ...route.params, slug: 'all' },
                     query: { ...route.query, page: 1 }
                  }"
                  v-slot="{ isExactActive }"
              >

                <label class="check-label">

                  <input type="checkbox"
                         class="check-input"
                         :checked="isExactActive"
                         :disabled="isExactActive"
                         value="All">

                  <span class="btn btn-white-dark"> All </span>

                </label>

              </router-link>

            </div>

            <template v-if="props.data.length > 1">
              <div v-for="( item, index ) in props.data" :key="index" class="col">

                <router-link
                    :to="{
                     name: 'dealsStore',
                     params: { ...route.params, slug: item.slug },
                     query: { ...route.query, page: 1 }
                  }"
                    v-slot="{ isExactActive }"
                >

                  <label class="check-label">

                    <input type="checkbox"
                           class="check-input"
                           :checked="isExactActive"
                           :disabled="isExactActive"
                           :value="item.department_name"
                    >

                    <span class="btn btn-white-dark active"> {{ item.department_name }} </span>

                  </label>

                </router-link>

              </div>
            </template>

          </div>

        </div>

      </div>

    </div>

  </header>


</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {useRoute} from "vue-router";
import {defineProps} from "vue";

export default {
  name: "DealsDepartmentsComponent"
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


</script>

<style scoped>

</style>