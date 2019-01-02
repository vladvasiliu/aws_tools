<template>
  <b-card header="Volumes">
    <b-list-group flush>
      <b-list-group-item
        v-for="volume in volumes_for_instance(instance)"
        :key="volume.id">{{ volume_name(volume) }}</b-list-group-item>
    </b-list-group>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    instance: {
      type: Object,
      default: () => {}
    }
  },

  computed: {
    ...mapGetters([
      'volumes_for_instance',
      'volume_name'
    ])
  }
}
</script>
