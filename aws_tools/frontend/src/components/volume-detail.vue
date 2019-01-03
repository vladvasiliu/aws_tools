<template>
  <div class="container-fluid mh-100">
    <Error
      v-if="error"
      v-bind="error"/>
    <Loading
      v-else-if="loading"
      message="Loading snapshots..."/>
    <volume-detail-snapshots
      v-if="snapshots"
      :snapshots="snapshots"/>
  </div>
</template>

<script>
import AxiosInstance from '@/api/'
import Loading from './loading'
import Error from './error'
import VolumeDetailSnapshots from './volume-detail-snapshots'

export default {
  name: 'VolumeDetail',
  components: {
    Error,
    Loading,
    VolumeDetailSnapshots
  },
  props: {
    volume: {
      type: Object,
      default () { return {} }
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
    AxiosInstance
      .get(this.volume.url)
      .then(response => {
        this.snapshots = response.data.ebssnapshot_set
      })
      .catch(error => {
        console.log(error)
        if (!error.response) {
          this.error = error
        } else {
          switch (error.response.status) {
            case 404:
              this.error = { message: 'No snapshots found.' }
              break
            default:
              this.error = { message: error.response.statusText }
          }
        }
      })
      .finally(() => {
        this.loading = false
      })
  }
}
</script>

<style scoped>

</style>
