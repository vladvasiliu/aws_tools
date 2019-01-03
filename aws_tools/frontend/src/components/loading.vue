<template>
  <div class="container-fluid text-center m-5 w-auto">
    <div class="col">
      <font-awesome-icon
        :icon="icon"
        spin
        class="display-4" />
      <div class="text-secondary font-weight-light font-italic mt-3">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import { faSpinner } from '@fortawesome/free-solid-svg-icons'

export default {
  name: 'Loading',
  props: {
    message: {
      type: String,
      default () { return 'Loading...' }
    }
  },
  data () {
    return {
      icon: faSpinner
    }
  }
}
</script>

<style scoped>

</style>
