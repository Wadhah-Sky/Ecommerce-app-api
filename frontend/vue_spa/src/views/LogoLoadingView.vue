<template>

  <div class="container">

    <div class="loading display-1">
      <div class="loading-text">
        <span class="loading-text-words">J</span>
        <span class="loading-text-words">A</span>
        <span class="loading-text-words">M</span>
        <span class="loading-text-words">I</span>
        <span class="loading-text-words">E</span>
        <span class="loading-text-words"> & </span>
        <span class="loading-text-words">C</span>
        <span class="loading-text-words">A</span>
        <span class="loading-text-words">S</span>
        <span class="loading-text-words">S</span>
        <span class="loading-text-words">I</span>
        <span class="loading-text-words">E</span>
      </div>
    </div>

  </div>


</template>

<script>

export default {
  name: "LogoLoadingView"
}

/*
  Define functions
*/
const setPageTitle = (title) => {
  /**
   * set a given title string as the webpage title.
   */
  document.title = title;
};

/*
  call functions
*/
setPageTitle("Jamie & Cassie | Loading");

</script>

<style scoped lang="scss">

//@import url(https://fonts.googleapis.com/css?family=Quattrocento+Sans);

@mixin position-center($text-align: center) {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  text-align: $text-align;
}

.loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #fff;
  z-index: 9999;
  font-size:7.6vw;
}

.loading-text {
  @include position-center;
  width: 100%;
  height: 100px;
  line-height: 100px;
  span {
    display: inline-block;
    margin: 0 5px;
    color: #0F1111;
    //font-family: 'Quattrocento Sans', sans-serif;
    // set loop from 0 to (number of span - 1)
    @for $i from 0 through 11 {
      &:nth-child(#{$i + 1}) {
        filter: blur(0px);
        // use calc($i/5) instead of (#{$i/5})
        animation: blur-text 1.5s calc($i/5)+s infinite linear alternate;
      }
    }
  }
}

@keyframes blur-text {
  0% {filter: blur(0px);}
  100% {filter: blur(4px);}
}

</style>