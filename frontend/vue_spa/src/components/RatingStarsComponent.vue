<template>

  <div class="row mt-1">

    <form>
      <div class="rating">

        <input type='radio' hidden name='no-rate' id='no-rate' data-idx='0'>
        <label id='no-rate' for='no-rate' @click="noRate">
          <span>I don't care</span>
          <font-awesome-icon icon="fa-solid fa-circle-xmark"/>
        </label>

        <input type='radio' hidden name='rate' id='rating_opt5' data-idx='1'>
        <label for='rating_opt5'><span>5 stars</span></label>

        <input type='radio' hidden name='rate' id='rating_opt4' data-idx='2'>
        <label for='rating_opt4'><span>4 stars & up</span></label>

        <input type='radio' hidden name='rate' id='rating_opt3' data-idx='3'>
        <label for='rating_opt3'><span>3 stars & up</span></label>

        <input type='radio' hidden name='rate' id='rating_opt2' data-idx='4'>
        <label for='rating_opt2'><span>2 stars & up</span></label>

        <input type='radio' hidden name='rate' id='rating_opt1' data-idx='5'>
        <label for='rating_opt1'><span>1 star & up</span></label>
      </div>
    </form>
  </div>

</template>

<script>
/*
  Libraries, methods, variables and components imports
*/
import {onMounted, ref} from "vue";

export default {
  name: "RatingStarsComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
const elementRateList = ref();

/*
  Define functions
*/
const noRate = () => {
  /**
   * Method to uncheck all the selected radio buttons.
   */

  // Loop over the list of element.
  for (let ele of elementRateList.value){
    // uncheck each element by set checked attribute of the element to be false.
    ele.checked = false;
  }
};

// When the view is mounted we can reach the 'document' object.
onMounted( () =>{
  elementRateList.value = document.getElementsByName("rate");
});

</script>

<style scoped lang="scss">

.rating {
  display: inline-block;
  font-size: 0;
  position: relative;
  text-transform: capitalize;
  padding: 0 0 8%;
  color: gray;

  label#no-rate {
    display: inline-block;
    margin-left: 8px;
    float: right;
    padding: 0;
    font-size: 24px;
    cursor: pointer;

    &::before {
      display: inline-block;
      transition: 0.3s;
    }

    span {
      opacity: 0;
      position: absolute;
      left: 0;
      bottom: 0;
      width: 100%;
      text-align: center;
      height: 20px;
      font-size: 1rem;
      white-space: nowrap;
      transition: 0.15s ease-out;
      pointer-events: none;
      letter-spacing: -2px;
      transform: translateY(-50%);
    }

    &:hover {
      span {
        opacity: 1;
        transform: none;
        letter-spacing: 0;
      }

      &::before {
        color: rgb(204, 12, 57);
        opacity: .6;
        filter: drop-shadow(0 0 4px);
      }

      & ~ *::before {
        color: rgb(204, 12, 57);
        opacity: .6;
        filter: drop-shadow(0 0 4px);
      }
    }
  }

  label:not([id="no-rate"]) {
    display: inline-block;
    float: right;
    padding: 0;
    font-size: 24px;
    cursor: pointer;

    &::before {
      content: "\2606";
      display: inline-block;
      transition: 0.3s;
    }

    span {
      opacity: 0;
      position: absolute;
      left: 0;
      bottom: 0;
      width: 100%;
      text-align: center;
      height: 20px;
      font-size: 1rem;
      white-space: nowrap;
      transition: 0.15s ease-out;
      pointer-events: none;
      letter-spacing: -2px;
      transform: translateY(-50%);
    }

    &:hover {
      span {
        opacity: 1;
        transform: none;
        letter-spacing: 0;
      }

      &::before {
        //content: "\2605";
        color: rgb(204, 12, 57);
        opacity: .6;
        filter: drop-shadow(0 0 4px);
      }

      & ~ *::before {
       // content: "\2605";
        color: rgb(204, 12, 57);
        opacity: .6;
        filter: drop-shadow(0 0 4px);
      }
    }
  }

  input:not([id="no-rate"]) {
    &:checked ~ label::before {
      content: "\2605";
      color: orange;
      filter: drop-shadow(0 0 4px);
      transform: rotate(.2turn);
      transition-delay: calc(0.1 * attr(data-idx integer));
    }
  }
}

.fa-circle-xmark:hover{
  color: #0F1111;
  transition: 0.3s;
  transform: scale(110%);
}

</style>