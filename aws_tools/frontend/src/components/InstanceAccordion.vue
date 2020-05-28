<template>
  <b-container>
    <b-row class="mb-3">
      <b-col>
        <instance-detail
          :instance="instance"
          :schedule-list="scheduleList"
        />
      </b-col>
    </b-row>
    <b-row>
      <div class="col">
        <volume-list
          :instance="instance"
          class="h-100"
        />
      </div>
    </b-row>
  </b-container>
</template>

<script>
import InstanceDetail from './instanceDetail'
import VolumeList from './volumeList'
import { Instance } from '../store/modules/instance'

export default {
  name: 'InstanceAccordion',
  components: {
    InstanceDetail,
    VolumeList
  },
  props: {
    instance: { type: Instance, default: null },
    scheduleList: { type: Array, required: true }
  }
}
</script>
