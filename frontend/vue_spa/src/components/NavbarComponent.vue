<template>

  <header class="section-header">
<!--    <nav class="navbar p-md-0 navbar-expand-sm navbar-light border-bottom">-->
<!--      <div class="container">-->
<!--        <button class="navbar-toggler" type="button" data-toggle="collapse"-->
<!--                data-target="#navbarTop4" aria-controls="navbarNav"-->
<!--                aria-expanded="false" aria-label="Toggle navigation">-->
<!--          <span class="navbar-toggler-icon"></span>-->
<!--        </button>-->
<!--        <div class="collapse navbar-collapse" id="navbarTop4">-->
<!--          <ul class="navbar-nav mr-auto">-->
<!--            <li class="nav-item dropdown">-->

<!--              <a href="#" class="nav-link"> English </a>-->

<!--            </li>-->
<!--            <li class="nav-item dropdown">-->

<!--              <a href="#" class="nav-link"> USD </a>-->

<!--            </li>-->
<!--          </ul>-->
<!--          <ul class="navbar-nav">-->
<!--            <li><a href="#" class="nav-link"> <i class="fa fa-envelope"></i>-->
<!--              Email </a></li>-->
<!--            <li><a href="#" class="nav-link"> <i class="fa fa-phone"></i> Call-->
<!--              us </a></li>-->
<!--          </ul> &lt;!&ndash; list-inline //  &ndash;&gt;-->
<!--        </div> &lt;!&ndash; navbar-collapse .// &ndash;&gt;-->
<!--      </div> &lt;!&ndash; container //  &ndash;&gt;-->
<!--    </nav>-->

    <section class="header-main border-bottom">
      <div class="container">
        <div class="row">
          <div class="col-3">
            <router-link :to="{name: 'home'}" class="brand-wrap">
              <img class="logo" src="../assets/images/logo/logo.png">
            </router-link> <!-- brand-wrap.// -->
          </div>
<!--          <div class="col-2">-->
<!--            <div class="dropdown">-->
<!--              <button class="btn btn-primary dropdown-toggle"-->
<!--                      type="button"-->
<!--                      id="dropdownMenuButton1"-->
<!--                      data-bs-toggle="dropdown"-->
<!--                      aria-expanded="false"-->
<!--              >-->
<!--                <i class="fa fa-bars"></i> All category-->
<!--              </button>-->
<!--              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">-->
<!--                <li>-->
<!--                  <a class="dropdown-item" href="#">Men's Fashion </a>-->
<!--                </li>-->
<!--                <li>-->
<!--                  <a class="dropdown-item" href="#">Women's Fashion </a>-->
<!--                </li>-->
<!--                <li>-->
<!--                  <a class="dropdown-item" href="#">Kids Fashion </a>-->
<!--                </li>-->
<!--              </ul>-->
<!--            </div>  &lt;!&ndash; category-wrap.// &ndash;&gt;-->
<!--          </div> &lt;!&ndash; col.// &ndash;&gt;-->
<!--          <div class="col-2">-->
<!--            <a href="/store" class="btn btn-outline-primary">Store</a>-->
<!--          </div>-->

          <div class="col-6">
            <form action="#" class="search">
              <div class="input-group w-10">
                <input type="text" class="form-control" style="width:60%;"
                       placeholder="Search">

                <div class="input-group-append">
                  <button class="btn btn-primary" type="submit">
                    <i class="fa fa-search"></i>
                  </button>
                </div>
              </div>
            </form> <!-- search-wrap .end// -->
          </div> <!-- col.// -->
          <div class="col-3">
            <div class="d-flex justify-content-end mb-3 mb-lg-0">
<!--              <div class="widget-header">-->
<!--                <small class="title text-muted">Welcome guest!</small>-->
<!--                <div>-->
<!--                  <a href="./signin.html">Sign in</a> <span-->
<!--                    class="dark-transp"> | </span>-->
<!--                  <a href="./register.html"> Register</a>-->
<!--                </div>-->
<!--              </div>-->
              <a href="./cart.html" class="widget-header pl-3 ml-3">
                <div class="icon icon-sm rounded-circle border">
                  <font-awesome-icon icon="fa-solid fa-shopping-cart" />
                </div>
                <span class="badge badge-pill badge-danger notify">0</span>
              </a>
            </div> <!-- widgets-wrap.// -->
          </div> <!-- col.// -->
        </div> <!-- row.// -->
      </div> <!-- container.// -->
    </section> <!-- header-main .// -->

  </header> <!-- section-header.// -->

</template>

<script>

export default {
  name: "NavbarComponent"
}

</script>

<script setup>

</script>

<style scoped>

</style>