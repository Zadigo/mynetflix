<template>
  <section id="search" class="container">
    <div class="row">
      <div class="col-sm-12 col-md-8 offset-md-2">
        <v-card elevation="0">
          <v-card-text>
            <h1 class="text-center mb-5">Movie Database</h1>
            <search-input :use-chips="false" />
          </v-card-text>
        </v-card>
      </div>
    </div>
  </section>
</template>

<script>
import SearchInput from '@/components/SearchInput.vue'

export default {
  name: 'HomeView',
  components: {
    SearchInput
  }
}
</script>

<style scoped>
section {
  margin-top: 100px;
}
</style>
