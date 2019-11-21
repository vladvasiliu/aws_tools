<template>
  <div class="row">
    <div class="col-auto">
      <instance-detail :instance="instance" />
    </div>
    <div class="col">
      <volume-list
        :instance="instance"
        class="h-100"
      />
    </div>
  </div>
</template>

<script>
import InstanceDetail from './instanceDetail'
import VolumeList from './volumeList'

export default {
  name: 'InstanceAccordion',
  components: {
    InstanceDetail,
    VolumeList
  },
  props: {
    instance: { type: Object, default: null }
  }
}
</script>
