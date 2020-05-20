<template>
  <b-card v-if="schedule">
    <template v-slot:header>
      <b-row>
        <b-col>
          <strong>{{ schedule.name }}</strong>
          <b-badge
            v-if="isLocalModified"
            class="ml-3"
            variant="warning"
            pill
          >
            Modified
          </b-badge>
        </b-col>
        <b-col
          align-self="end"
          md="4"
        >
          <b-row
            class="mt-n1 mb-n1"
          >
            <b-col>
              <b-button
                size="sm"
                :disabled="!isLocalModified"
                :variant="isLocalModified ? 'outline-primary' : 'outline-secondary'"
                block
                @click="cancelChanges"
              >
                Cancel
              </b-button>
            </b-col>
            <b-col>
              <b-button
                size="sm"
                :disabled="!isLocalModified"
                :variant="isLocalModified ? 'primary' : 'outline-secondary'"
                block
                @click="saveChanges"
              >
                Save
              </b-button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </template>
    <div class="row mb-3">
      <div class="col col-auto">
        <strong>Status: </strong>
        <b-form-checkbox
          v-model="local_schedule.active"
          name="status-button"
          inline
          switch
        >
          {{ local_schedule.active ? "Active" : "Disabled" }}
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
              v-for="hour in hourRange()"
              :key="hour"
            >
              <b-th>{{ hour }}:00</b-th>
              <b-td
                v-for="day in dayRange()"
                :key="day * 24 + hour"
                :variant="schedule.schedule[day * 24 + hour] | state_to_variant"
                class="text-center"
                @click="updateScheduleAction(day, hour)"
              >
                {{ schedule.schedule[day * 24 + hour] | state_to_text }}
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
import { _ } from 'vue-underscore'

function range (size) {
  return [...Array(size).keys()]
}

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
  data: function () {
    return {
      local_schedule: { ...this.schedule }
    }
  },
  computed: {
    isLocalModified: function () {
      return !_.isEqual(this.local_schedule, this.schedule)
    }
  },
  watch: {
    schedule: function (newVal) {
      // console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.local_schedule = { ...newVal }
    }
  },
  methods: {
    updateScheduleAction: function (day, hour) {
      console.log(day, hour)
    },
    dayRange: () => range(7),
    hourRange: () => range(24),
    cancelChanges: function () {
      this.local_schedule = Object.assign({}, this.schedule)
    },
    saveChanges: function () {
      this.$emit('scheduleChange', this.local_schedule)
    }
  }
}
</script>

<style scoped>

</style>
