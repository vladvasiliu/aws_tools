<template>
  <b-card v-if="schedule">
    <template v-slot:header>
      <strong>{{ schedule.name }}</strong>
    </template>
    <div class="row mb-3">
      <div class="col col-auto">
        <strong>Status: </strong>
        <b-form-checkbox
          :checked="schedule_status"
          name="status-button"
          inline
          switch
          @change="updateScheduleStatus"
        >
          {{ schedule.active ? "Active" : "Disabled" }}
        </b-form-checkbox>
      </div>
    </div>
    <div class="row">
      <div class="col col-auto">
        <b-table-simple
          hover
          small
        >
          <b-thead>
            <b-tr>
              <b-th />
              <b-th>Mon</b-th>
              <b-th>Tue</b-th>
              <b-th>Web</b-th>
              <b-th>Thu</b-th>
              <b-th>Fri</b-th>
              <b-th>Sat</b-th>
              <b-th>Sun</b-th>
            </b-tr>
          </b-thead>
          <b-tbody>
            <b-tr
              v-for="hour in 24"
              :key="hour"
            >
              <b-th>{{ hour - 1 }}:00</b-th>
              <b-td
                v-for="day in 7"
                :key="(day-1) * 24 + hour - 1"
                :variant="schedule.schedule[(day-1) * 24 + hour-1] | state_to_variant"
                class="text-center"
              >
                {{ schedule.schedule[(day-1) * 24 + hour-1] | state_to_text }}
              </b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </div>
    </div>
  </b-card>
  <div
    v-else
    class="text-center"
  >
    Please select a schedule
  </div>
</template>

<script>
export default {
  name: 'ScheduleDetail',
  filters: {
    state_to_variant: function (value) {
      switch (value) {
        case 0:
          return ''
        case 1:
          return 'success'
        case 2:
          return 'danger'
        default:
          return 'warning'
      }
    },
    state_to_text: function (value) {
      switch (value) {
        case 0:
          return '-'
        case 1:
          return 'on'
        case 2:
          return 'off'
        default:
          return 'unknown'
      }
    }
  },
  props: {
    schedule: { type: Object, default: null, required: false }
  },
  computed: {
    schedule_status: function () {
      return this.schedule.active
    }
  },
  methods: {
    updateScheduleStatus: function (value) {
      this.$emit('scheduleStatusChange', value)
    }
  }
}
</script>

<style scoped>

</style>
