<template>
  <nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <router-link :to="{ name: 'home_view' }" class="navbar-brand fw-bold text-uppercase">
        <span class="text-primary me-1">Movie</span> Database
      </router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'BaseNavbar'
}
</script>
