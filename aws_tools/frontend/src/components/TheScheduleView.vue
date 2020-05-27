<template>
  <div class="row">
    <div class="col-3">
      <ObjectListGroupCard
        card-title="Schedules"
        :show-all="false"
        :object-error="schedules_error"
        :object-list="schedules"
        :route-dest="routeDest"
      />
    </div>
    <div class="col">
      <router-view />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'
import ObjectListGroupCard from './ObjectListGroupCard'

export default {
  name: 'TheScheduleView',
  components: {
    ObjectListGroupCard
  },
  computed: {
    ...mapGetters(['schedules', 'schedules_error']),
    faExclamationTriangle () { return faExclamationTriangle }
  },
  created () {
    this.$store.dispatch('LOAD_SCHEDULE_LIST')
  },
  methods: {
    routeDest: (schedule) => ({ name: 'ScheduleViewID', params: { id: schedule.id } }),

    select: function (object) {
      this.selectedSchedule = object
    },

    scheduleChange: function (newSchedule) {
      const newValue = {
        schedule: this.selectedSchedule,
        changes: {
          active: newSchedule.active,
          schedule: newSchedule.schedule
        }
      }
      this.$store.dispatch('UPDATE_SCHEDULE', newValue)
    }
  }
}
</script>

<style scoped>

</style>
