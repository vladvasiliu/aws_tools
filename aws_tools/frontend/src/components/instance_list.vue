<template>
  <b-card header="Instances">
    <b-list-group flush>
      <b-list-group-item
        v-b-toggle="instance.id"
        v-for="instance in instances_for_selected_account"
        :key="instance.id"
        action
        class="flex-column align-items-start">
        {{ instance._name }}
        <b-collapse
          :id="instance.id"
          class="w-100 align-self-center">
          <div
            class="d-flex m-3 justify-content-left"
            @click.stop>
            <instanceDetail
              :instance="instance"
              class="m-1"/>
            <volumeList
              :instance="instance"
              class="m-1"/>
          </div>
        </b-collapse>
      </b-list-group-item>
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
  }
}
</script>
