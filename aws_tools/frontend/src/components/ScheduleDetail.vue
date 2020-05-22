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
    <b-row>
      <b-col
        sm="5"
        md="5"
        lg="4"
      >
        <b-table-simple
          borderless
          small
        >
          <b-tbody>
            <b-tr>
              <b-th>Status</b-th>
              <b-td>
                <b-form-checkbox
                  v-model="local_schedule.active"
                  name="status-button"
                  inline
                  switch
                >
                  {{ local_schedule.active ? "Active" : "Disabled" }}
                </b-form-checkbox>
              </b-td>
            </b-tr>
            <b-tr>
              <b-th>Instances</b-th>
              <b-td>{{ local_schedule.instance_count }}</b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </b-col>
      <b-col
        sm="auto"
      >
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
                :key="interval(day, hour)"
                :variant="local_schedule.schedule[interval(day, hour)] | state_to_variant"
                class="text-center"
                @click="updateScheduleAction(day, hour)"
              >
                {{ local_schedule.schedule[interval(day, hour)] | state_to_text }}
              </b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </b-col>
    </b-row>
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

function localScheduleFromSelected (selectedSchedule) {
  if (selectedSchedule === null) { return null }
  const result = _.clone(selectedSchedule)
  result.schedule = [...selectedSchedule.schedule]
  return result
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
      local_schedule: localScheduleFromSelected(this.schedule)
    }
  },
  computed: {
    isLocalModified: function () {
      return !(_.isEqual(this.local_schedule.schedule, this.schedule.schedule) && _.isEqual(this.local_schedule.active, this.schedule.active))
    }
  },
  watch: {
    schedule: function (newVal) {
      this.local_schedule = localScheduleFromSelected(newVal)
    }
  },
  methods: {
    updateScheduleAction: function (day, hour) {
      const interval = this.interval(day, hour)
      const oldVal = this.local_schedule.schedule[interval]
      this.$set(this.local_schedule.schedule, interval, (oldVal + 1) % 3)
    },
    dayRange: () => _.range(7),
    hourRange: () => _.range(24),
    interval: (day, hour) => day * 24 + hour,
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
