<template>
  <base-site>
    <template #default>
      <video-row :items="store.movies" title="My row 1" />
      <video-row :items="store.movies" title="My row 2" />
    </template>
  </base-site>
</template>

<script>
import { useMovies } from '@/store/movies'

import BaseSite from '@/layouts/BaseSite.vue'
import VideoRow from '@/components/VideoRow.vue'

export default {
  name: 'VideosView',
  components: {
    BaseSite,
    VideoRow
  },
  setup () {
    const store = useMovies()
    return {
      store
    }
  }
}
</script>
