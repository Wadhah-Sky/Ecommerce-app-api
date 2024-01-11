<template>

  <div class="row">
    <div class="col-md-9">

      <header class="section-heading">
        <h3 class="section-title">Customer Reviews </h3>

      </header>

      <article class="box mb-3">
        <div class="icontext w-100">
          <img src="https://www.vhv.rs/dpng/d/295-2956244_individual-icon-png-individual-icon-transparent-png.png"
               class="img-xs icon rounded-circle">
          <div class="text">
            <span class="date text-muted float-md-right">28.07.2022</span>
            <h6 class="mb-1">Mike John</h6>

          </div>
        </div> <!-- icontext.// -->
        <div class="mt-3">
          <p>
            It has exceeded my expectations and I would highly recommend it to others.
          </p>
        </div>
      </article>

      <article class="box mb-3">
        <div class="icontext w-100">
          <img src="https://icons.veryicon.com/png/o/miscellaneous/conventional-use/personal-43.png"
               class="img-xs icon rounded-circle">
          <div class="text">
            <span class="date text-muted float-md-right">24.10.2023</span>
            <h6 class="mb-1">Jason A</h6>

          </div>
        </div> <!-- icontext.// -->
        <div class="mt-3">
          <p>
            The product I purchased is simply amazing. It has greatly improved my daily life and I can't imagine going without it now.
          </p>
        </div>
      </article>


    </div> <!-- col.// -->
  </div> <!-- row.// -->


</template>

<script>
export default {
  name: "ProductReviewsComponent"
}
</script>

<style scoped>
@media (min-width: 280px) and (max-width: 767px) {
  .section-title{
    font-size: 17px;
  }
}
</style>