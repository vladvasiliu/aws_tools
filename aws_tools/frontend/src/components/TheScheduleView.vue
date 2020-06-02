<template>
  <b-row align-h="between">
    <b-col cols="3">
      <ObjectListGroupCard
        card-title="Schedules"
        :show-all="false"
        :object-error="schedules_error"
        :object-list="schedules"
        :route-dest-fun="routeDestFun"
        :route-dest-add="routeDestAdd"
      />
    </b-col>
    <b-col>
      <router-view
        @scheduleDelete="scheduleDelete"
        @scheduleChange="scheduleChange"
      />
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'
import ObjectListGroupCard, { RouteDest } from './ObjectListGroupCard'

export default {
  name: 'TheScheduleView',
  components: {
    ObjectListGroupCard
  },
  data: function () {
    return {
      routeDestAdd: new RouteDest('Add', { name: 'ScheduleViewNew' })
    }
  },
  computed: {
    ...mapGetters(['schedules', 'schedules_error']),
    faExclamationTriangle () { return faExclamationTriangle }
  },
  created () {
    this.$store.dispatch('SCHEDULE_LOAD_LIST')
  },
  methods: {
    routeDestFun: (schedule) => ({ name: 'ScheduleViewID', params: { id: schedule.id } }),

    scheduleChange: function (schedule) {
      const newValue = {
        schedule: schedule,
        changes: {
          active: schedule.active,
          schedule: schedule.schedule,
          name: schedule.name
        }
      }
      this.$store.dispatch('SCHEDULE_UPDATE', newValue).then(
        newSchedule => {
          this.$bvToast.toast(schedule.name + ' was successfully saved', {
            title: 'Schedule saved',
            solid: true,
            variant: 'info',
            isStatus: true
          })
          this.$router.replace({ name: 'ScheduleViewID', params: { id: newSchedule.id } }).catch(() => {})
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
            title: 'Failed to save schedule',
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
