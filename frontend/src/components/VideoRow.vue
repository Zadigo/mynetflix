<template>
  <div class="row my-3">
    <h5 class="fw-bold">{{ title }}</h5>
    <div class="videos">
      <div class="left" @click="left">
        <font-awesome-icon icon="fa-solid fa-arrow-left" />
      </div>
      
      <div class="right" @click="right">
        <font-awesome-icon icon="fa-solid fa-arrow-right" />
      </div>

      <div ref="wrapper" class="wrapper">
        <div v-for="item in items" :key="item.id" class="video">
          <router-link :to="{ name: 'video_view', params: { id: item.id, lang: $i18n.locale } }" class="d-block h-100">
            <img src="https://via.placeholder.com/250x150" class="img-fluid" alt="">          
          </router-link>
          <!-- <div class="preview"></div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useScroll } from '@vueuse/core'

export default {
  name: 'VideoRow',
  components: {

  },
  props: {
    title: {
      type: String,
      required: true
    }, 
    items: {
      type: Array,
      default: () => []
    }
  },
  setup () {
    const target = null
    const { directions, x } = useScroll(target)
    return {
      target,
      scrollX: x,
      directions
    }
  },
  mounted () {
    this.target = this.$refs.wrapper
  },
  methods: {
    left () {},
    right () {}
  }
}
</script>

<style scoped>
.videos {
  position: relative;
  width: 100%;
  max-width: 100%;
  height: auto;
  margin-top: .5rem;
  margin-bottom: .5rem;
  /* box-sizing: content-box; */
}

.videos .wrapper {
  width: 100%;
  background-color: #fff;
  overflow-x: scroll;
  /* padding: .5rem; */
  /* margin: 1rem; */
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  scrollbar-width: none;
  /* box-sizing: content-box; */
}

.wrapper::-webkit-scrollbar {
  /* width: 5px; */
  display: none;
}

/* .videos::-webkit-scrollbar-track {
  background: rgba(38, 38, 38, .5);
}

.videos::-webkit-scrollbar-thumb {
  background: rgba(38, 38, 38, .5);
}

.videos::-webkit-scrollbar-thumb:hover {
  background: #555;
} */

.videos .video {
  position: relative;
  transition: all .4s ease;
  height: 150px;
  width: 250px;
  overflow: hidden;
  min-width: 250px;
  background-color: green;
  cursor: pointer;
  z-index: 10;
}

.videos .video:first-child {
  margin-left: 1rem;
}

.videos .video:last-child {
  margin-right: 1rem;
}

.videos .preview {
  position: absolute;
  overflow: hidden;
  width: 100%;
  height: 100%;
  cursor: pointer;
  top: 0;
  left: 0;
  background-color: red;
  z-index: -1;
}

.videos .video:hover {
  overflow: visible;
}

.videos .video:hover .preview {
  height: 300px;
  width: 250px;
  box-shadow: 0 .5rem 1rem rgba(0, 0, 0, .15) !important;
  transform: scale(1.1, 1.1);
  z-index: 1000;
}

.videos .video:not(:last-child) {
  margin-right: .15rem;
}

.left,
.right {
  background-color: rgba(38, 38, 38, .3);
  transition: background-color .4s ease;
  height: 100%;
  width: auto;
  min-width: 50px;
  cursor: pointer;
  color: white;
  font-weight: bold;
  text-align: center;
  vertical-align: middle;
  font-size: 1.5rem;
  padding: .5rem;
  z-index: 15;
}

.left svg,
.right svg {
  margin-top: 3.5rem;
  margin-bottom: auto;
  font-size: 1.7rem;
}

.left:hover,
.right:hover {
  font-weight: 700;
  background-color: rgba(38, 38, 38, .5);
}

.left {
  position: absolute;
  top: 0;
  left: 0;
}

.right {
  position: absolute;
  top: 0;
  right: 0;
}
</style>

