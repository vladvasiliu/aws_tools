<template>
  <div class="container-fluid text-center m-5 w-auto">
    <div class="col text-danger">
      <font-awesome-icon
        id="error-icon"
        :icon="icon"
        :size="iconSize"
      />
      <b-popover
        v-if="tooltip"
        target="error-icon"
        triggers="hover"
      >
        <template v-slot:title>
          {{ error.message }}
        </template>
        <div
          v-if="error.details"
          style="white-space: pre-wrap"
        >
          {{ error.details }}
        </div>
      </b-popover>
      <div v-else>
        <div
          class="font-weight-bold mt-3"
        >
          {{ error.message }}
        </div>
        <div
          v-if="error.details"
          class="text-secondary font-italic"
          style="white-space: pre-wrap"
        >
          {{ error.details }}
        </div>
        <div
          v-if="error.more"
          class="text-secondary font-italic"
          style="white-space: pre-wrap"
        >
          {{ error.more }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons'

export class Error {
  constructor (message = 'Something went wrong...', details = '', more = '') {
    this.message = message
    this.details = details
    this.more = more
  }
}

export default {
  name: 'ErrorView',
  props: {
    error: { type: Error, default: new Error() },
    tooltip: { type: Boolean, default: false },
    iconSize: { type: String, default: '4x' }
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
