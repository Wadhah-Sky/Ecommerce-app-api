<template>

  <div class="row">

    <div class="col-md-12">

      <header class="section-heading">

        <h3>{{props.title}}</h3>

      </header>

      <main>

        <div class="content">

          <ul class="details-list-group">
            <li v-for="(val, index) in props.details" :key="index" :id="index" class="details-list-item">
              <span>
                <span class="details-list-item-attribute">
                  {{index}}
                </span>
                <span class="details-list-item-value">
                  {{val}}
                </span>
              </span>

            </li>
          </ul>

        </div>

      </main>

    </div> <!-- col.// -->

  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/

export default {
  name: "ProductDetailsComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  details: {
    type: Object,
    required: true
  }
});

</script>

<style scoped>

.details-list-group{
  margin: 0 0 1px 18px;
  padding: 0;
  color: #0f1111!important;
}

.details-list-item{
  list-style: none;
  margin-bottom: 5px;
  word-wrap: break-word;

}

.details-list-item-attribute{
  padding: 0;
  margin: 0;
  font-weight: 600;
}

.details-list-item-attribute:after{
  content: ':';
  margin: 0 5px 0 4px;
}

.details-list-item-value{
  padding: 0;
  margin: 0;
  font-weight: 400;
}

</style>