<template>
  <div id="ratings">
    <v-card v-for="(rating, i) in ratings" :key="i" class="mt-1">
      <v-card-text>
        <div class="d-flex justify-content-start gap-2">
          <span class="fw-bold">{{ rating.source }}</span>
          <span class="fw-light">{{ rating.rating }}</span>
        </div>

        <v-progress-linear v-if="rating.is_percentage" :model-value="rating.rating" class="mt-2" half-increments />
        <v-progress-linear v-else-if="rating.scale > 10" :model-value="rating.rating" class="mt-2" half-increments />
        <!-- <v-rating v-else :length="rating.scale" :model-value="rating.rating" class="mx-n5" color="yellow-darken-3" height="15" rounded readonly> -->
        <v-rating v-else v-model="rating.rating" :length="rating.scale" class="mt-2" height="15">
          <template v-slot:item="props">
            <v-icon :color="props.isFilled ? 'green' : 'grey-lighten-1'" size="large" @click="props.onClick">
              {{ props.isFilled ? 'mdi-star-circle' : 'mdi-star-circle-outline' }}
            </v-icon>
          </template>
        </v-rating>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'RatingBlock',
  props: {
    ratings: {
      type: String
    }
  },
  data () {
    return {
      colors: ['green', 'purple', 'orange', 'indigo', 'red']
    }
  }
}
</script>
