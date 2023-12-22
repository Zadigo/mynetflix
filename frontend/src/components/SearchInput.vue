<template>
  <div class="search-wrapper">
    <div class="d-flex justify-content-around align-items-center gap-2">
      <v-text-field v-model="requestParams.title" variant="solo" placeholder="Search movie name, actors..." hide-details @keypress.enter="handleSearch" />
      <v-btn color="primary" size="x-large" :disabled="cannotSearch" @click="handleSearch">
        Search
      </v-btn>
    </div>

    <div v-if="useChips" class="chips-wrapper">
      <v-chip-group class="mt-3">
        <v-chip v-for="search in previousSearch" :key="search" @click="handleChipSearch(search)">{{ search }}</v-chip>
      </v-chip-group>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { ref } from 'vue'
import { useMovies } from '@/store/movies'
import { storeToRefs } from 'pinia'

export default {
  name: 'SearchInput',
  props: {
    useChips: {
      type: Boolean,
      default: true
    }
  },
  emits: {
    'new-search' () {
      return true
    },
    'search-started' () {
      return true
    },
    'search-ended' () {
      return true
    }
  },
  setup () {
    const store = useMovies()
    const { currentMovie } = storeToRefs(store)
    const requestParams = ref({
      // API key
      // apikey: 'b7e2e7b5',
      // Movie title
      title: null,
      // Year
      release_year: null,
      // Response type
      movie_type: 'movie'
    })
    return {
      currentMovie,
      requestParams
    }
  },
  computed: {
    cannotSearch () {
      // When the user has entered no text value to search, disables
      // any element that needs to be disabled
      return this.requestParams.title === null || this.requestParams.title === ''
    },
    previousSearch () {
      // Return the six previous searched values
      let values = this.sessionStorage.search || []
      values = _.uniq(values)
      const returnValues = values.length > 0 ? values : []
      return returnValues.slice(returnValues.length - 6, returnValues.length)
    }
  },
  methods: {
    async handleSearch () {
      // Handle the request to the OMDB api
      try {
        this.$emit('search-started', true)
        // const response = await this.$omdb.get('/', { params: this.requestParams })
        const response = await this.$http.post('movies/search', this.requestParams)
        this.currentMovie = response.data
        this.$session.create('currentMovie', this.currentMovie)
        
        if (this.$route.name !== 'search_view') {
          this.$router.push({ name: 'search_view' })
        }
        
        this.$session.defaultList('search', this.requestParams.t)
        if (response.data?.Title) {
          this.$session.defaultList('movies', response.data)
        }
        
        this.$emit('search-ended', true)
        this.$emit('new-search')
      } catch (e) {
        console.log(e)
      }
    },
    handleChipSearch (search) {
      // Handle the request to the OMDB api
      // when the user clicks on a chip
      this.requestParams.t = search
      this.handleSearch()
    }
  }
}
</script>
