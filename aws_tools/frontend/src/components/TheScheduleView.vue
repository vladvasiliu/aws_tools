<template>
  <div class="row">
    <div class="col-3">
      <ObjectListGroupCard
        card-title="Schedules"
        :show-all="false"
        :object-error="schedules_error"
        :object-list="schedules"
        :selected-object="selectedSchedule"
        @selectObject="select"
      />
    </div>
    <div class="col">
      <ScheduleDetail
        :schedule="selectedSchedule"
        @scheduleStatusChange="scheduleStatusChange"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'
import ObjectListGroupCard from './ObjectListGroupCard'
import ScheduleDetail from './ScheduleDetail'

export default {
  name: 'TheScheduleView',
  components: {
    ObjectListGroupCard,
    ScheduleDetail
  },
  data: function () {
    return {
      selectedSchedule: null
    }
  },
  computed: {
    ...mapGetters(['schedules', 'schedules_error']),
    faExclamationTriangle () { return faExclamationTriangle }
  },
  created () {
    this.$store.dispatch('LOAD_SCHEDULE_LIST')
  },
  methods: {
    select: function (object) {
      this.selectedSchedule = object
    },

    scheduleStatusChange: function (value) {
      const newValue = {
        schedule: this.selectedSchedule,
        changes: {
          active: value,
        }
      }
      console.log(newValue)
      this.$store.dispatch('UPDATE_SCHEDULE', newValue)
    }
  }
}
</script>

<style scoped>

</style>
