<template>
  <b-card v-if="schedule">
    <template
      v-slot:header
    >
      <strong>{{ schedule.name }}</strong>
    </template>
    <div class="row">
      <div class="col col-auto">
        <strong>Status:</strong>
        <b-form-checkbox
          v-model="schedule_status"
          name="status-button"
          switch
        >
          {{ schedule_status ? "Active" : "Disabled" }}
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
    schedule_status: {
      get () {
        return this.schedule.active
      },
      set (value) {
        this.$emit('scheduleStatusChange', value)
      }
    }
  }
}
</script>

<style scoped>

</style>
