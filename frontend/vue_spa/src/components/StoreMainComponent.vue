<template>

  <div class="row pt-3">

    <main v-if="!storePagination.dataLoading" class="col-md-12" >

        <header class="border-bottom mb-3 ms-0 pb-2">
          <div class="row row-cols-auto">

              <div class="col data-count" >
                <span>
                  {{ storePagination.dataCount }} {{ storePagination.dataCount > 1 ? 'items' : 'item' }} found
                </span>

              </div>

              <div class="col ps-0">

                <span style="margin-right: 5px">
                  <font-awesome-icon :icon="['fa-solid', 'fa-sliders']" />
                  Filters
                </span>

                <div class="button r" id="button-filter" @click="emits('toggle-filter-side-panel')">
                  <input type="checkbox" class="checkbox" :checked="storeFilter.collapsed"/>
                  <div class="knobs"></div>
                  <div class="layer"></div>
                </div>

              </div>

          </div>

          <div>
            <materialize-chips-component :store-filter="storeFilter" />
          </div>

        </header><!-- sect-heading -->

      <template v-if="storePagination.dataResult.length > 0">

        <div class="row">

          <div v-for="( product, index ) in storePagination.dataResult"
               :key="index"
               class="col-md-3"
          >

            <product-card-component :product-title="product.title"
                                    :product-items-count="product.product_items_count"
                                    :rating="product.rating"
                                    :product-slug="product.slug"
                                    :product-item-slug="product.product_item.slug"
                                    :product-item-attr="product.product_item.attributes.join()"
                                    :thumbnail="product.product_item.thumbnail"
                                    :price-currency-symbol="product.product_item.price_currency_symbol"
                                    :list-price-amount="product.product_item.list_price_amount"
                                    :deal-price-amount="product.product_item.deal_price_amount"
                                    :promotion-title="product.product_item.promotion_title"
                                    :promotion-summary="product.product_item.promotion_summary"
            />

          </div> <!-- col.// -->


        </div> <!-- row end.// -->

        <pagination-component :store-pagination="props.storePagination"/>

      </template>

      <template v-else>

        <no-result-found-component/>

      </template>

    </main> <!-- col.// -->

    <content-loader-component v-else style="transition: all 0.3s ease-in-out" />

  </div>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import ContentLoaderComponent from "@/components/ContentLoaderComponent";
import NoResultFoundComponent from "@/components/NoResultFoundComponent";
import PaginationComponent from "@/components/PaginationComponent";
import ProductCardComponent from "@/components/ProductCardComponent";
import MaterializeChipsComponent from "@/components/MaterializeChipsComponent";
import { toRef, defineProps, defineEmits} from "vue";

export default {
  name: "StoreMainComponent",
  components: {
    ContentLoaderComponent,
    NoResultFoundComponent,
    PaginationComponent,
    ProductCardComponent,
    MaterializeChipsComponent
  }
}

</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  storePagination: {
    type: Object,
    required: true
  },
  storeFilter: {
    type: Object,
    required: true
  }
});
const storeFilter = toRef(props, 'storeFilter');
// Define the list of events that you want to emit.
const emits = defineEmits(['toggle-filter-side-panel']);

/*
  Define functions
*/

/*
  call functions
*/

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
//
// watch(storePagination.dataResult, (oldVal, newVal) => {
//     console.log('watch',data.value)
// },
//     {immediate: true},
//     {deep: true},
//
// );

</script>

<style scoped>

.data-count:after{
  content: "|";
  padding-left: 6px;
}

.knobs,
.layer {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}

.button {
  position: relative;
  top: 30%;
  width: 45px;
  height: 22px;
  margin: -20px auto 0 auto;
  overflow: hidden;
  display: inline-block;
}

.button.r,
.button.r .layer {
  border-radius: 100px;
}

.checkbox {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 3;
}

.knobs {
  z-index: 2;
}

.layer {
  width: 100%;
  background-color: grey;
  transition: 0.5s ease all;
  z-index: 1;
}

#button-filter .knobs:before {
  content: "";
  position: absolute;
  top: 2px;
  left: 1px;
  width: 17px;
  height: 17px;
  color: #0F1111;
  font-size: 10px;
  font-weight: bold;
  text-align: center;
  line-height: 1;
  padding: 4px 2px;
  background-color: #fff;
  border-radius: 50%;
  transition: 0.5s ease all, 0.5s left cubic-bezier(0.18, 0.89, 0.35, 1.15);
}

#button-filter .checkbox:active + .knobs:before {
  width: 46px;
  border-radius: 50%;
}

#button-filter .checkbox:checked:active + .knobs:before {
  margin-left: -26px;
}

#button-filter .checkbox:checked + .knobs:before {
  content: "";
  color: #0F1111;
  top: 2px;
  right: 2px;
  left: 27px;
  background-color: #fff;
}

#button-filter .checkbox:checked ~ .layer {
  background-color: #0F1111;
}

/*input[type=checkbox]{*/
/*  height: 0;*/
/*  width: 0;*/
/*  visibility: hidden;*/
/*}*/

/*label {*/
/*  cursor: pointer;*/
/*  text-indent: -9999px;*/
/*  width: 48px;*/
/*  height: 26px;*/
/*  background: grey;*/
/*  border-radius: 100px;*/
/*  position: relative;*/
/*}*/

/*label:after {*/
/*  content: '';*/
/*  position: absolute;*/
/*  top: 5px;*/
/*  left: 5px;*/
/*  width: 16px;*/
/*  height: 16px;*/
/*  background: #fff;*/
/*  border-radius: 90px;*/
/*  transition: 0.3s;*/
/*}*/

/*input:checked + label {*/
/*  background: #0F1111;*/
/*}*/

/*input:checked + label:after {*/
/*  left: calc(100% - 5px);*/
/*  transform: translateX(-100%);*/
/*}*/

/*label:active:after {*/
/*  width: 30px;*/
/*}*/

</style>