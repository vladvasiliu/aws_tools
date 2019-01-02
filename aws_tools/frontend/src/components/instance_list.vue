<template>
  <b-card header="Instances">
    <b-list-group
      flush>
      <template
        v-for="instance in instances_for_selected_account">
        <b-list-group-item
          v-b-toggle="instance.id"
          :key="instance.id"
          action
          class="border-top-1 border-bottom-0 m-0">
          {{ instance._name }}
        </b-list-group-item>

        <b-collapse
          :id="instance.id"
          :key="instance.id + 'detail'"
          class="w-100 align-self-center mb-2">
          <b-list-group-item
            class="d-flex justify-content-left"
            @click.stop>
            <instanceDetail
              :instance="instance"
              class="m-1"/>
            <volumeList
              :instance="instance"
              class="m-1"/>
          </b-list-group-item>
        </b-collapse>
      </template>
    </b-list-group>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

import volumeList from './volumeList.vue'
import instanceDetail from './instanceDetail.vue'

export default {
  components: {
    volumeList, instanceDetail
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
