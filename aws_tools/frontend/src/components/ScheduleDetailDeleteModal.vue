<template>
  <b-modal
    :id="modalId"
    header-bg-variant="danger"
    header-text-variant="light"
    title="Delete schedule?"
    ok-title="Delete"
    ok-variant="danger"
    size="lg"
    @ok="$emit('confirm-delete')"
  >
    <h5>Confirm deletion of schedule: <strong class="text-danger font-italic">{{ schedule.name }}</strong></h5>
    <br>
    <b-alert
      :variant="schedule.instance_count ? 'warning' : 'info'"
      show=""
      class="text-center"
    >
      <BIconExclamationTriangleFill v-if="schedule.instance_count" />
      <BIconInfoCircle v-else />
      There {{ scheduleCountMsg }} using this schedule.
    </b-alert>
  </b-modal>
</template>

<script>
import { BIconExclamationTriangleFill, BIconInfoCircle } from 'bootstrap-vue'
import { Schedule } from '../store/modules/schedule'

export default {
  name: 'ScheduleDetailDeleteModal',
  components: {
    BIconExclamationTriangleFill,
    BIconInfoCircle
  },
  props: {
    modalId: { type: String, required: true },
    schedule: { type: Schedule, required: true }
  },
  computed: {
    scheduleCountMsg: function () {
      switch (this.schedule.instance_count) {
        case 0:
          return 'are no instances'
        case 1:
          return 'is one instance'
        default:
          return 'are ' + this.schedule.instance_count + ' instances'
      }
    }
  }
}
</script>

<style scoped>

</style>
