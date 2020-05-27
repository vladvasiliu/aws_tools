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
