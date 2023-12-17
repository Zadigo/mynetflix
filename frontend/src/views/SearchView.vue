<template>
  <section id="search">
    <header id="movie-header" ref="header" class="px-4 py-5 mb-5 text-center shadow-sm">
      <!-- <h1 class="display-5 fw-bold text-body-emphasis">Centered hero</h1> -->
      <div class="col-lg-6 mx-auto">
        <search-input id="search" @new-search="handleHeaderImage" />
      </div>
      <!-- <div class="background-blur"></div>
      <div ref="header" class="background-image-wraper"></div> -->
    </header>

    <div class="container my-5">
      <!-- <span>{{ currentMovie }}</span> -->
      <div class="row">
        <div class="col-sm-12 col-md-12">
          
          <div class="row mt-2">
            <div class="col-sm-12 col-md-8">
              <!-- Movie Information -->
              <div class="row">
                <div class="col-sm-12 col-md-12">
                  <v-card>
                    <v-card-item>
                      <v-card-title><h1 class="text-uppercase">{{ currentMovie.Title }}</h1></v-card-title>
                      <v-card-subtitle class="d-flex justify-content-start gap-2">
                        <span class="fw-bold text-body-secondary">{{ currentMovie.Year }}</span>
                        <span class="fw-light text-body-secondary">({{ currentMovie.Released }})</span>
                        <span class="fw-light text-body-emphasis">{{ currentMovie.Genre }}</span>
                      </v-card-subtitle>
                    </v-card-item>

                    <v-card-text>
                      <v-card-actions>
                        <v-btn variant="tonal" class="mt-2">
                          <font-awesome-icon :icon="['fas', 'bookmark']"></font-awesome-icon>
                          Bookmark
                        </v-btn>
                      </v-card-actions>
                    </v-card-text>
                  </v-card>
                </div>
              </div>

              <div class="row mt-3">
                <h2 class="h5">Cast</h2>
                <div v-for="actor in actors" :key="actor" class="col-sm-12 col-md-3">
                  <v-card>
                    <v-card-text>
                      {{ actor }}
                    </v-card-text>
                  </v-card>
                </div>
              </div>
  
              <div class="row my-3">
                <div class="col-sm-12 col-md-12">
                  <h2 class="h5">Plot</h2>
                  <v-card>
                    <v-card-text>
                      <p>{{ currentMovie.Plot }}</p>
                    </v-card-text>
                  </v-card>
                </div>
              </div>
              
              <!-- Ratings -->
              <div class="row">
                <h2 class="h5">Ratings</h2>
                <div class="col-sm-12 col-md-12">
                  <v-card class="mt-1">
                    <v-card-text>
                      <div class="d-flex justify-content-start gap-2">
                        <span class="fw-bold">IMDB</span>
                        <span class="fw-light">{{ currentMovie.imdbRating }}</span>
                      </div>
                      <v-rating half-increments readonly :length="10" :size="20" :model-value="parseFloat(currentMovie.imdbRating)" active-color="primary" class="mt-2" />
                    </v-card-text>
                  </v-card>

                  <v-card v-for="(rating, i) in currentMovie.Ratings" :key="i" class="mt-1">
                    <v-card-text>
                      <div class="d-flex justify-content-start gap-2">
                        <span class="fw-bold">{{ rating.Source }}</span>
                        <span class="fw-light">{{ rating.Value }}</span>
                      </div>
                      <v-rating v-if="rating.Source === 'Internet Movie Database'" half-increments readonly :length="parseRating(rating.Value)[1]" :size="20" :model-value="parseRating(rating.Value)[0]" active-color="primary" class="mt-2" />
                      <v-progress-linear v-if="rating.Source === 'Rotten Tomatoes' || rating.Source === 'Metacritic'" :model-value="rating.Value" class="mx-n5" color="yellow-darken-3" height="20" rounded></v-progress-linear>
                    </v-card-text>
                  </v-card>
                </div>
              </div>
            </div>
          
            <div class="col-sm-12 col-md-4">
              <v-card>
                <v-img :src="currentMovie.Poster" aspect-ratio="1/1" />
              </v-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { useMovies } from '@/store/movies'
import { storeToRefs } from 'pinia'
import SearchInput from '@/components/SearchInput.vue'

export default {
  name: 'SearchView',
  components: {
    SearchInput
  },
  beforeRouteEnter (from, to, next) {
    next(vm => {
      if (vm.store.currentMovie.Title === null) {
        vm.$router.push({ name: 'home_view' })
      }
    })
  },
  setup () {
    const store = useMovies()
    const { currentMovie } = storeToRefs(store)
    return {
      store,
      currentMovie
    }
  },
  computed: {
    actors () {
      return this.currentMovie.Actors?.split(',')
    }
  },
  beforeMount () {
    if (!this.store.hasCurrentMovie) {
      this.currentMovie = this.$session.retrieve('currentMovie') || {}
    }
  },
  mounted () {
    this.handleHeaderImage()
  },
  methods: {
    handleHeaderImage () {
      this.$refs.header.style.backgroundImage = `url(${this.currentMovie.Poster})`
    },
    parseRating (value) {
      return value.split('/')
    }
  }
}
</script>

<style scoped>
/* section {
  margin-top: 100px;
} */

#movie-header {
  position: relative;
  background-size: cover;
  background-repeat: no-repeat;
  background-position-y: center;
  background-blend-mode: difference;
}

#search {
  z-index: 9999;
}

.background-blur {
  z-index: 20;
  background-color: rgba(0, 0, 0, .1);
  filter: blur(2px);
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}
.background-image-wraper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-repeat: no-repeat;
  background-position-y: center;
  background-blend-mode: difference;
  z-index: 10;
}
</style>
