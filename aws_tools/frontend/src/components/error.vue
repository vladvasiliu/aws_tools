<template>
  <div class="container-fluid text-center m-5 w-auto">
    <div class="col text-danger">
      <font-awesome-icon
        :icon="icon"
        class="display-4"
      />
      <div
        class="font-weight-bold mt-3"
      >
        {{ message }}
      </div>
      <div
        v-if="details"
        class="text-secondary font-italic"
      >
        {{ details }}
      </div>
    </div>
  </div>
</template>

<script>
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons'

export default {
  name: 'Error',
  props: {
    message: {
      type: String,
      default () { return 'Something went wrong...' }
    },
    details: {
      type: String,
      default () { return '' }
    }
  },
  data () {
    return {
      icon: faExclamationCircle
    }
  }
}
</script>

<style scoped>

</style>
