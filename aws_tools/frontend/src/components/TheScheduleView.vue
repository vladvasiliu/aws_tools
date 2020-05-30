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
      <router-view
        @scheduleDelete="scheduleDelete"
        @scheduleChange="scheduleChange"
      />
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
    this.$store.dispatch('SCHEDULE_LOAD_LIST')
  },
  methods: {
    routeDest: (schedule) => ({ name: 'ScheduleViewID', params: { id: schedule.id } }),

    scheduleChange: function (newSchedule) {
      const newValue = {
        schedule: newSchedule,
        changes: {
          active: newSchedule.active,
          schedule: newSchedule.schedule
        }
      }
      this.$store.dispatch('SCHEDULE_UPDATE', newValue).then(
        () => {
          this.$bvToast.toast(newSchedule.name + ' was successfully saved', {
            title: 'Schedule updated',
            solid: true,
            variant: 'info',
            isStatus: true
          })
        },
        err => {
          const h = this.$createElement
          const message = h(
            'p',
            {},
            [
              h('strong', {}, newSchedule.name + ':'),
              h('div', {}, err.message)
            ]
          )
          this.$bvToast.toast([message], {
            title: 'Failed to update schedule',
            solid: true,
            variant: 'warning'
          })
        }
      )
    },

    scheduleDelete: function (schedule) {
      this.$store.dispatch('SCHEDULE_DELETE', schedule).then(
        () => {
          this.$bvToast.toast(schedule.name + ' was successfully deleted', {
            title: 'Schedule deleted',
            solid: true,
            variant: 'info',
            isStatus: true
          })
          this.$router.push({ name: 'ScheduleView' })
        },
        err => {
          const h = this.$createElement
          const message = h(
            'p',
            {},
            [
              h('strong', {}, schedule.name + ':'),
              h('div', {}, err.message)
            ]
          )
          this.$bvToast.toast([message], {
            title: 'Failed to delete schedule',
            solid: true,
            variant: 'warning'
          })
        }
      )
    }
  }
}
</script>

<style scoped>

</style>
