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
          class="border-top-1 border-bottom-0 m-0 d-flex justify-content-between align-items-center instance-name">
          {{ instance.name }}
          <font-awesome-icon
            :icon="collapseIcon"
            class="instance-name-caret" />
        </b-list-group-item>

        <b-collapse
          :id="instance.id"
          :key="instance.id + 'detail'"
          class="w-100 align-self-center mb-2">
          <b-list-group-item
            class="d-flex justify-content-left">
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
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'

import instanceDetail from './instanceDetail.vue'
import volumeList from './volumeList'

export default {
  components: {
    instanceDetail,
    volumeList
  },
  data () {
    return {
      collapseIcon: faCaretDown
    }
  },
  computed: {
    ...mapGetters([
      'instances_for_selected_account'
    ])
  },
  created () {
    this.$store.dispatch('LOAD_INSTANCE_LIST')
      .then(() => {
      })
  }
}
</script>

<style>
.instance-name:hover .instance-name-caret {
  opacity: inherit;
}
.instance-name .instance-name-caret {
  opacity: 0.3;
}
.instance-name.collapsed .instance-name-caret {
  transform: rotate(90deg);
}
</style>
