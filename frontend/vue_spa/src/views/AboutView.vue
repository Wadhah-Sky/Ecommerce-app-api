<template>

  <section class="section-content mt-3">

    <div class="container pb-4 mb-4">

      <div class="row pt-3">

        <main class="col-md-12">

          <header class="mb-3 ms-0 pb-2" style="text-align: center; justify-content: center; align-content: center">
            <h4>Who we are?</h4>
          </header>

          <div class="row" style="text-align: left; justify-content: left;">

              <div class="col-12 info-details">

                <p>
                  We are an online retailer dedicated to bringing you the best products at affordable prices.
                  With a focus on quality and customer satisfaction, we strive to provide exceptional service
                  and an enjoyable shopping experience. Our team is passionate about innovation and staying
                  up-to-date with the latest trends to bring you the most sought-after items. We value our
                  customers and are committed to building lasting relationships. Thank you for choosing us as
                  your go-to destination for online shopping.
                </p>

              </div>

          </div>

        </main>
      </div>
    </div>
  </section>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import {scrollTopSmooth} from "@/assets/javascript/smothScroll";
import {onMounted} from "vue";

export default {
  name: "AboutView"
}
</script>

<script setup>

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};

// Life cycles
onMounted(() => {
  // Scroll the browser's window up.
  scrollTopSmooth(window.scrollY, 300, "ease-in-out");
});

/*
  call functions
*/
setPageTitle("Jamie & Cassie | About");

</script>

<style scoped>

.info-details{
  font-size: 16px;
}

</style>