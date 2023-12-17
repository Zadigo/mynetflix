<template>
  <section>
    <header>
      <nav class="navbar"></nav>
    </header>

    <div :style="`background-image: url(${require('@/assets/back1.jpg')});`" class="bg-image col-xxl-8 px-4 py-5 text-light">
      <div class="row flex-lg-row-reverse align-items-center g-5 py-5">
        <div class="col-10 col-sm-8 col-lg-6">
          <img src="bootstrap-themes.png" class="d-block mx-lg-auto img-fluid" alt="Bootstrap Themes" width="700" height="500" loading="lazy">
        </div>
        <div class="col-lg-6">
          <h1 class="display-5 fw-bold lh-1 mb-3">Responsive left-aligned hero with image</h1>
          <p class="lead">Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.</p>
          <div class="d-grid gap-2 d-md-flex justify-content-md-start">
            <router-link :to="{ name: 'video_view', params: { id: 1, lang: $i18n.locale } }" class="btn btn-primary btn-lg px-4 me-md-2">
              <font-awesome-icon icon="fa-solid fa-play" class="me-2" />
              Play
            </router-link>
            <button type="button" class="btn btn-outline-secondary btn-lg px-4">Default</button>
          </div>
        </div>
      </div>
      <!-- <div class="mask"></div> -->
    </div>

    <div class="container-fluid">
      <slot></slot>
    </div>
  </section>
</template>

<script>
// import BaseNavbar from '@/layouts/bootstrap/BaseTimeline.vue'
export default {
  name: 'BaseSite',
  components: {

  }
}
</script>

<style scoped>
.bg-image {
  position: relative;
  background-position-y: 30%;
}
</style>
