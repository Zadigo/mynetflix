import { defineStore } from 'pinia'
// import moviesData from '@/data/movies.json'
// import _ from 'lodash'

const useMovies = defineStore('movies', {
  // state () {
  //   return {
  //     movies: moviesData,
  //     currentMovie: null
  //   }
  // },
  // actions: {
  //   getMovie (id) {
  //     this.currentMovie = _.find(this.movies, ['id', id * 1])
  //   }
  // }

  state: () => ({
    movies: [],
    currentMovie: {}
  }),
  getters: {
    hasCurrentMovie () {
      if (typeof this.currentMovie.Title ==='undefined') {
        return false
      } else {
        return true
      }
    }
  }
})

export {
  useMovies
}
