<template>
  <fragment>
    <b-list-group-item
      v-b-toggle="instance.id"
      :key="instance.id"
      action
      class="border-top-1 border-bottom-0 m-0 d-flex justify-content-between align-items-center">
      {{ instance._name }}
      <font-awesome-icon
        :icon="collapse"
        size="lg"
        variant="light"
        class="text-secondary" />
    </b-list-group-item>

    <b-collapse
      :id="instance.id"
      :key="instance.id + 'detail'"
      v-model="visible"
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
  </fragment>
</template>

<script>
import { Fragment } from 'vue-fragment'
import { faCaretLeft, faCaretDown } from '@fortawesome/free-solid-svg-icons'

import instanceDetail from './instanceDetail.vue'
import volumeList from './volumeList'

export default {
  name: 'InstanceListDetail',
  components: {
    Fragment,
    instanceDetail,
    volumeList
  },
  props: {
    instance: {
      type: Object,
      default: () => {
      }
    }
  },
  data: () => {
    return {
      visible: false
    }
  },
  computed: {
    collapse () {
      return this.visible ? faCaretDown : faCaretLeft
    }
  }
}
</script>
