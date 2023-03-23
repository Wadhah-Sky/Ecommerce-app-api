<template>

  <div class="container">

    <div class="scroll-menu">

      <div class="row">
        <!--  <div class="description">-->
        <!--    <h3>Expandable Breadcrumbs</h3>-->
        <!--    <p>Perfect for pages with long titles</p>-->
        <!--  </div>-->

        <div class="col-md-12">

          <ul class="breadcrumbs">
            <li class="first">
              <router-link :to="{ name: 'home' }">
                <font-awesome-icon :icon="['fa-solid', 'fa-house']"/>
              </router-link>
            </li>

            <router-link
                v-for="( item, index ) in props.data" :key="index"
                :to="{
                name: route.name,
                params:{ slug: item.slug },
                query: {
                  minPrice: route.query.minPrice,
                  maxPrice: route.query.maxPrice,
                  selectBy: route.query.selectBy,
                  page: 1
                }
              }"
                v-slot="{ href, navigate, isActive, isExactActive }"
                custom
            >
              <li :class="[ isActive ? 'last active' : '']"
                  :tabindex="isActive ? -1 : 0"

              >
                <a :href="href"
                   :class="[isActive ? 'router-link-active' : '', isExactActive ? 'router-link-exact-active' : '']"
                   @click="navigate"
                   :style="[ isActive ? { pointerEvents: 'none', display: 'inline-block' } : {width: `${75}px`}]"
                   @mouseover="isActive ? '' : removeWidth($event.currentTarget)"
                   @mouseout="isActive ? '' : setWidth($event.currentTarget)"
                >
                  {{ item.title }}
                </a>

              </li>

            </router-link>

          </ul>
        </div>

      </div>

    </div>

  </div>

</template>

<script>

/*
  Libraries, methods, variables and components imports
*/
import {defineProps} from "vue";
import {useRoute} from "vue-router";

export default {
  name: "BreadCrumbsComponent"
}
</script>

<script setup>

/*
  Define handlers (properties, props and computed)
*/
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const props = defineProps({
  data: {
    type: Array,
    required: true
  }
});
const route = useRoute();

/*
  Define functions
*/
const removeWidth = (ele) => {
  /**
   * Remove the width property from the element, so the clientWidth value will
   * be in action.
   */
  ele.style.removeProperty('width');
};
const setWidth = (ele) => {
  /**
   * Set fixed width value to the element width property.
   */
  ele.style.setProperty('width', `${75}px`);
};

// const setCrumbsProperties = (crumbs) => {
//   /**
//    * Method to set properties and events to certain list of DOM node elements.
//    */
//
//   // Loop over each of the elected <a> element.
//   for (let node of crumbs){
//
//     /*
//      Info: In the HTML DOM (Document Object Model), an HTML document is a collection
//            of nodes with (or without) child nodes, can be categorized:
//
//            1- Nodes: are element nodes, text nodes, and comment nodes, whitespace between
//                      elements are also text nodes.
//
//            2- Elements: are only element nodes, e.g. any html tag element.
//     */
//     /*
//      Info: If you want to get parent node of specific element, you have two properties:
//
//            1- <target>.parentNode : will return html element.
//
//            2- <target>.parentElement : will return html element.
//
//            * The only difference is that parentElement returns null if the parent node
//              is not an element node.
//     */
//
//     // Get the parent node of the current node.
//     let parent = node.parentNode
//
//     // Check if the parent node is <li> element.
//     if (parent.matches('li')){
//
//       // We DON'T want to make any change to the <a> node that his parent <li>
//       // have class (first) or (active).
//       if ( !( parent.classList.contains('active') || parent.classList.contains('first') ) ){
//
//         /*
//           Info: There are multiple ways to get value of calculation for width
//                 of element depending on (padding, borders ..etc):
//                 1- clientWidth: is the inner width (i.e. the space inside
//                    an element including padding but excluding borders and
//                    scrollbars).
//                 2- offsetWidth: is the outer width (i.e. the space occupied by
//                    the element, including padding and borders).
//          */
//         // Get the clientWidth value.
//         let nodeWidth = node.clientWidth;
//
//         // Set width property to be 75px for current element.
//         node.style.setProperty('width', `${75}px`);
//
//         node.addEventListener( 'mouseover', function handler() {
//           // Set the clientWidth value to the element width property.
//           node.style.setProperty('width', `${nodeWidth}px`);
//         });
//         node.addEventListener( 'mouseout', function handler() {
//           // Set the fixed width value to the element width property.
//           node.style.setProperty('width', `${75}px`);
//         });
//       }
//     }
//   }
// };

// When the view is mounted we can reach the 'document' object.
// onMounted( () => {
//
//   // Select specific list of html element from the DOM.
//   const crumbs = document.querySelectorAll(".breadcrumbs li a");
//
//   // call a function.
//   setCrumbsProperties(crumbs);
//
// });

// Before the view being changed.
// onBeforeUpdate( () =>{
//
//   // Select specific list of html element from the DOM.
//   const crumbs = document.querySelectorAll(".breadcrumbs li a");
//
//   for (let node of crumbs){
//     console.log('Node:', node.style.width)
//     node.style.removeProperty('width');
//     node.removeEventListener( 'mouseover', function handler(){} );
//     node.removeEventListener( 'mouseout', function handler(){} );
//   }
// });

// When the view is changed.
// onUpdated( () => {
//
//   // Select specific list of html element from the DOM.
//   const crumbs = document.querySelectorAll(".breadcrumbs li a");
//
//   // Call a function.
//   setCrumbsProperties(crumbs);
// });


</script>

<style scoped lang="scss">

$black: #0F1111;

div.scroll-menu {
  overflow: auto;
  white-space: nowrap;
}

div.scroll-menu::-webkit-scrollbar {
    display: none; /* for Chrome, Safari and Opera */
}

div.scroll-menu{
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

div.scroll-menu .row {
  display: inline-block;
  margin-right: 11px;
}

@mixin inline {
	display: inline-block;
	*display: inline;
	zoom: 1;
	vertical-align: top;
}

.description {
  padding-left: 15px;
  border-left: 2px solid #000;

  h3 {
    font-weight:300;
    font-size: 20px;
    line-height: 20px;
    margin: 0px;
    color: #fff;
    text-transform: uppercase;
  }

  p {
    margin-top: 10px;
    font-weight:300;
  }
}

.wrapper {
  margin: 50px;
}

ul.breadcrumbs {
	margin: 25px 0px 0px;
	padding: 0px;
	font-size: 0px;
	line-height: 0px;
	@include inline;
	height: 40px;

	li {
		position: relative;
		margin: 0px 0px;
		padding: 0px;
		list-style: none;
		//list-style-image: none;
		@include inline;
		border-left: 1px solid #ccc;
		transition: 0.6s ease all;

		&:hover {
			&:before {
				border-left: 10px solid #e9ecef;
        transition: 0.6s ease all;
			}

			a {
				color: $black;
				background: #e9ecef;
        transition: 0.6s ease all;
			}

		}

		&:before {
			content:"";
			position: absolute;
			right: -9px;
			top: -1px;
			z-index: 20;
			border-left: 10px solid #fff;
			border-top: 22px solid transparent;
			border-bottom: 22px solid transparent;
      transition: 0.6s ease all;
		}

		&:after {
			content:"";
			position: absolute;
			right: -10px;
			top: -1px;
			z-index: 10;
			border-left: 10px solid #ccc;
			border-top: 22px solid transparent;
			border-bottom: 22px solid transparent;
      transition: 0.6s ease all;
		}


		&.active {

			a {
				color: #fff;
				background: $black;
			}
		}

		&.first {
			border-left: none;

			a {
				font-size: 18px;
				padding-left: 20px;
				border-radius: 5px 0px 0px 5px;
			}
		}

		&.last {

			&:before {
				display: none;
			}
			&:after {
				display: none;
			}

			a {
				padding-right: 20px;
				border-radius: 0px 40px 40px 0px;
			}
		}

		a {
			display: block;
			font-size: 12px;
			line-height: 40px;
			color: #757575;
			padding: 0px 15px 0px 25px;
			text-decoration: none;
			background: #fff;
			border: 1px solid #ddd;
			white-space:nowrap;
			overflow: hidden;
			transition: 0.6s ease all;
		}
	}
}

</style>