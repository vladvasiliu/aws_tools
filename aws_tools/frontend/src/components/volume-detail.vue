<template>
  <div class="container-fluid mh-100">
    <Loading
      v-if="loading"
      message="Loading snapshots..."
    />
    <ErrorView
      v-else-if="error"
      :error="error"
    />
    <volume-detail-snapshots
      v-else
      :snapshots="snapshots"
    />
  </div>
</template>

<script>
import Loading from './loading'
import VolumeDetailSnapshots from './volume-detail-snapshots'
import { Error } from './ErrorView'

export default {
  name: 'VolumeDetail',
  components: {
    ErrorView: () => (import('./ErrorView')),
    Loading,
    VolumeDetailSnapshots
  },
  props: {
    volume: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      snapshots: null,
      loading: true,
      error: null
    }
  },
  mounted () {
    this.axios
      .get(this.volume.url)
      .then(response => {
        this.snapshots = response.data.ebssnapshot_set
        if (!this.snapshots.length) {
          this.error = new Error('No snapshots found')
        }
      })
      .catch(error => {
        let message = 'Failed to get snapshots'
        let other = ''
        if (error.response) {
          switch (error.response.status) {
            case 404:
              message = 'No snapshots found.'
              break
            default:
              other = error.response.data
          }
        }
        this.error = new Error(message, error.message, other)
      })
      .finally(() => {
        this.loading = false
      })
  }
}
</script>

<style scoped></style>
