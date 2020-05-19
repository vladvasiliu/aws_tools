<template>
  <b-card v-if="schedule">
    <template v-slot:header>
      <strong>{{ schedule.name }}</strong>
    </template>
    <div class="row">
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
