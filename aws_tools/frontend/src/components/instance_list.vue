<template>
  <b-card header="Instances">
    <b-list-group
      flush>
      <InstanceListDetail
        v-for="instance in instances_for_selected_account"
        :instance="instance"
        :key="instance.id"
      />
    </b-list-group>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

import InstanceListDetail from './instance-list-detail'

export default {
  components: {
    InstanceListDetail
  },
  computed: {
    ...mapGetters([
      'instances_for_selected_account'
    ])
  },
  created () {
    this.$store.dispatch('LOAD_INSTANCE_LIST')
      .then(() => {
        this.$store.dispatch('GET_ALL_VOLUMES')
      })
  }
}
</script>
