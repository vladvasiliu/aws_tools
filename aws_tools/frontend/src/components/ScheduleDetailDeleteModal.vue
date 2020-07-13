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
      :variant="scheduleUseCount ? 'warning' : 'info'"
      show=""
      class="text-center"
    >
      <BIconExclamationTriangleFill v-if="scheduleUseCount" />
      <BIconInfoCircle v-else />
      This schedule is {{ scheduleUseCount ? '' : 'not' }} in use.
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
    scheduleUseCount: function () {
      return this.schedule.instance_count + this.schedule.rds_instance_count + this.schedule.rds_cluster_count
    }
  }
}
</script>

<style scoped>

</style>
