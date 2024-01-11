<template>

  <!-- ========================= FOOTER ========================= -->
  <footer class="section-footer border-top">
    <div class="container">

      <section class="row footer-bottom border-top">

        <div class="col-sm-12 col-md-8 text-md-start">

          <div>
            <span class="px-2">
              <router-link :to="{name: 'contact'}" style="color: #212529; text-decoration: none">Contact</router-link>
            </span>

            <span class="px-2">
              <router-link :to="{name: 'about'}" style="color: #212529; text-decoration: none">About</router-link>
            </span>

            <span class="px-2">
              <router-link :to="{}" style="color: #212529; text-decoration: none">Terms</router-link>
            </span>

            <span class="px-2">
              <router-link :to="{}" style="color: #212529; text-decoration: none">FAQ</router-link>
            </span>
          </div>

        </div>

        <div class="col-sm-12 col-md-4 text-md-end">
          <p class="text-muted">© 2024 Jamie & Cassie All Rights Received</p>
        </div>

<!--        <div class="col-md-2 text-md-right text-muted">-->
<!--          <i class="fab fa-lg fa-cc-visa"></i>-->
<!--          <i class="fab fa-lg fa-cc-paypal"></i>-->
<!--          <i class="fab fa-lg fa-cc-mastercard"></i>-->
<!--        </div>-->

      </section>
    </div><!-- //container -->
  </footer>
  <!-- ========================= FOOTER END // ========================= -->

</template>

<script>

export default {
  name: "FooterComponent"
}

</script>

<script setup>

</script>

<style lang="scss" scoped>
// Customize the number of grid tiers of bootstrap

// override the default min-width value (576px) of .col-sm-* column to be 330px
// also you should set the of max-width to same column as breakpoint to .col-md-* which by default it's 768px
@media (max-width: 1000px) {
  .col-sm-12 {
    flex: 0 0 auto;
    width: 100%;
  }

  .col-sm-12 > *{
    text-align: center;
    justify-content: center;
    align-content: center;
    margin: 0 auto;
  }

  .px-2{
    margin: 0 auto;
    //display: block;
  }

  .col-sm-12 > p{
    font-size: 12.5px;
  }
}
</style>

<style scoped>

.px-2{
  display: inline-block;
}

.px-2:hover a{
  text-decoration: underline!important;
  color: #0f1111!important;
  transition: all 0.2s ease-in-out;
}
</style>