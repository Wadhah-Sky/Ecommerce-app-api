<template>

  <section class="page_404">
    <div class="container">
      <div class="row">
        <div class="col-sm-12 d-flex">
          <div class="col-sm-12 col-sm-offset-1 text-center">
            <div class="four_zero_four_bg">

              <h1 class="text-center">404</h1>

            </div>

            <div class="contant_box_404">
              <h3 class="h2">
                Look like you're lost
              </h3>

              <p>The page you are looking for is not available!</p>

              <router-link :to="{name: 'home'}" :class="['btn btn-home']"
              >
                  <span>
                    <font-awesome-icon :icon="['fa-solid', 'fa-house']" style="margin-right: 3px"/>
                    Back Home
                  </span>

              </router-link>

            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

</template>

<script>

/*
  Libraries, methods, properties and components imports
*/
// import {ref} from 'vue';

export default {
  name: "PageNotFoundView"
}

</script>

<script setup>

/*
  Define handlers (constants, props and computed)
*/
// const message = ref("404 - Not Found!");

/*
  Define functions
*/
const setPageTitle = async (title) => {
  /**
   * set a given title string as the webpage title.
   */
  // async make the function return a promise when it's done.
  return document.title = title;
};

/*
  call functions with top-level await, to trigger <suspense> in parent component.
*/
// await makes the function wait for a promise.
await setPageTitle('Jamie & Cassie | 404 - page not found');

</script>

<style scoped>

.btn {
  text-decoration: none;
  width: 100%;
  font-size: 1.1rem;
  margin-top: 4vh;
  padding: 1.5vh;
  border-radius: 3px;
}

.btn:focus {
  box-shadow: none;
  outline: none;
  color: white;
  -webkit-box-shadow: none;
  -webkit-user-select: none;
  transition: none;
}

.btn:hover, a.disabled {
  background-color: #e9ecef;
  color: #0F1111;
}

.btn-home{
  color: #fff;
  background-color: #0F1111;
  border-color: #0F1111;
  width: 170px!important;
}

.btn-home:hover{
  background-color: #fff!important;
  color: #0F1111;
  border-color: #0F1111;
}

a.disabled{
  pointer-events: none;
}

a:active{
  transform: translateY(3%);
  transition: transform 0.2s;
}

/*======================
    404 page
=======================*/

.page_404{
  padding:40px 0;
  background:#fff;
  justify-content: center;
}

.page_404  img{
  width:100%;
}

.four_zero_four_bg{
  background-image: url(https://cdn.dribbble.com/users/285475/screenshots/2083086/dribbble_1.gif);
  height: 400px;
  background-position: center;
  object-fit: contain;
  -o-object-fit: contain;
}

.four_zero_four_bg h1{
  font-size:80px;
}

.four_zero_four_bg h3{
  font-size:80px;
}

/*.link_404{*/
/*  color: #fff!important;*/
/*  padding: 10px 20px;*/
/*  background: #39ac31;*/
/*  margin: 20px 0;*/
/*  display: inline-block;*/
/*}*/

.contant_box_404{
  margin-top:-50px;
}

</style>