<template>

  <section class="section-content mt-3">

    <div class="container border-bottom pb-4">

      <div class="row pt-3" style="text-align: center; justify-content: center; align-content: center">

        <main class="col-md-12">

          <header class="mb-3 ms-0 pb-2">
            <h4>Contact</h4>
          </header>

          <div class="row">

              <div class="col-12 info-details">
                <font-awesome-icon style="color: #0f1111; vertical-align: middle" icon="fa-solid fa-envelope"/>
                <a href="mailto:<info@jamieandcassie.store>?subject=Contact-us" style="color: #212529">
                  info@jamieandcassie.store
                </a>
              </div>

              <div class="col-12 info-details mt-2">
                <font-awesome-icon style="color: #0f1111; vertical-align: middle" icon="fa-solid fa-phone"/>
                  +111-2222-3333
              </div>

              <div class="col-12 info-details mt-4">
                <a href="https://www.facebook.com/" id="icon-facebook" title="facebook" class="me-4" target="_blank" style="color: #0f1111; text-decoration: none !important; text-underline: none; font-size: 17px; text-align: center;">
                  <font-awesome-icon icon="fa-brands fa-facebook-f"/>
                </a>

                <a href="https://instagram.com/" id="icon-instagram" title="instagram" class="me-4" target="_blank" style="color: #0f1111; text-decoration: none !important; text-underline: none; font-size: 17px; text-align: center;">
                  <font-awesome-icon icon="fa-brands fa-instagram"/>
                </a>

                <a href="https://www.youtube.com/" id="icon-youtube" title="youtube" target="_blank" style="color: #0f1111; text-decoration: none !important; text-underline: none; font-size: 17px; text-align: center;">
                  <font-awesome-icon icon="fa-brands fa-youtube"/>
                </a>

              </div>

          </div>

        </main>

      </div>

    </div>

  </section>

  <section class="map_sec">
        <div class="container">
            <div class="row">
                <div class="col-md-10 offset-md-1">
                    <div class="map_inner">
                        <h4 class="mb-3">Find Us on Google Map</h4>
                        <p>
                          <font-awesome-icon style="color: #0f1111; vertical-align: middle" icon="fa-solid fa-location-dot"/>
                          Karada, Baghdad, 10069
                        </p>
                        <div class="map_bind">
                            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d26678.37098794469!2d44.4249773!3d33.297989799999996!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x155781bc7ed270e1%3A0x151cf02d7b87ca2f!2sKarada%2C%20Baghdad!5e0!3m2!1sen!2siq!4v1697668128494!5m2!1sen!2siq"
                                    loading="lazy"
                                    referrerpolicy="no-referrer-when-downgrade"
                                    width="100%"
                                    height="450"
                                    style="border:0;"
                                    allowfullscreen=""
                                    aria-hidden="false"
                                    tabindex="0"
                            >
                            </iframe>
                        </div>
                    </div>
                </div>
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
  name: "ContactView"
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
setPageTitle("Jamie & Cassie | Contact");

</script>

<style scoped>

.info-details{
  font-size: 16px;
}

#icon-facebook:hover,
#icon-instagram:hover,
#icon-youtube:hover{
  transition: all 0.2s ease-in-out;
}

#icon-facebook:hover, #icon-facebook:active{
  color: #3b5998!important;
}

#icon-instagram:hover, #icon-instagram:active{
  color: #d62976!important;
}

#icon-youtube:hover, #icon-youtube:active{
  color: #c4302b!important;
}

.map_sec{
  padding: 50px 0px;
}
.map_inner h4, .map_inner p{
  color: #000;
  text-align: center
}
.map_inner p{
  font-size: 16px;
}
.map_bind{
  margin-top: 50px;
  border-radius: 8px;
  overflow: hidden;
}
</style>