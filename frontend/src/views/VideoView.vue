<template>
  <section id="video">
    <div class="container-fluid p-0">
      <base-video-player :video-url="require(`@/assets/${store.currentMovie.url}`)" />
      <!-- <base-video-player :video-url="require('@/assets/big1.mp4')" /> -->
    </div>
  </section>
</template>

<script>
import { useMovies } from '@/store/movies'

import BaseVideoPlayer from '@/layouts/bootstrap/players/BaseVideoPlayer.vue'

export default {
  name: 'VideoView',
  components: {
    BaseVideoPlayer
  },
  setup () {
    const store = useMovies()
    return {
      store
    }
  },
  beforeMount () {
    this.store.getMovie(this.$route.params.id)
  }
}
</script>

<style scoped>
body {
  overflow: hidden;
}
</style>
