<template>
  <section id="movies">
    <base-navbar />

    <v-app>
      <router-view :key="$route.name" />
      <!-- <router-view v-slot="{ Component }">
        <transition :key="$route.name" name="opacity" mode="in-out">
          <component :is="Component" />
        </transition>
      </router-view> -->
    </v-app>
  </section>
</template>

<script>
import BaseNavbar from './components/BaseNavbar.vue'

export default {
  name: 'App',
  components: {
    BaseNavbar
  }
}
</script>

<style>
.opacity-enter-active,
.opacity-leave-active {
  transition: all .3s ease-in-out;
}

.opacity-enter-from,
.opacity-leave-to {
  opacity: 0;
  transform: translateX(-100px);
}

.opacity-enter-to,
.opacity-leave-from {
  opacity: 1;
  transform: translateX(0px);
}
</style>
