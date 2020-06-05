<template>
  <b-card v-if="local_schedule">
    <template v-slot:header>
      <b-row>
        <b-col>
          <div v-if="!renaming">
            <strong>{{ local_schedule.name }}</strong>
            <b-badge
              v-if="isLocalModified"
              class="ml-3"
              variant="warning"
              pill
            >
              Modified
            </b-badge>
          </div>
          <b-form-input
            v-else
            v-model="local_schedule.name"
            autofocus
            class="mt-n2 mb-n2 h-100 d-inline-block"
            @blur="renaming = !renaming"
          />
        </b-col>
        <b-col
          align-self="end"
          cols="auto"
        >
          <b-button-toolbar class="mb-n2 mt-n2">
            <b-button
              :disabled="!isLocalModified"
              :variant="isLocalModified ? 'primary' : 'outline-secondary'"
              @click="saveChanges"
            >
              Save
            </b-button>
            <b-dropdown
              id="dropdown-1"
              variant="primary"
              split-variant="outline-primary"
              size="sm"
              right
              class="ml-1"
              @click="saveChanges"
            >
              <b-dropdown-item-button @click="renaming = !renaming">
                Rename
              </b-dropdown-item-button>
              <b-dropdown-item-button
                :disabled="!isLocalModified"
                block
                @click="cancelChanges"
              >
                Cancel changes
              </b-dropdown-item-button>
              <b-dropdown-divider />
              <b-dropdown-item-button
                v-b-modal:delete-modal-id
                variant="danger"
              >
                Delete
              </b-dropdown-item-button>
            </b-dropdown>
          </b-button-toolbar>
          <schedule-detail-delete-modal
            modal-id="delete-modal-id"
            :schedule="schedule"
            @confirm-delete="deleteSchedule"
          />
        </b-col>
      </b-row>
    </template>
    <b-row>
      <b-col
        lg="4"
      >
        <b-table-simple
          borderless
          small
          fixed
        >
          <b-tbody>
            <b-tr>
              <b-th>Status</b-th>
              <b-td class="text-left">
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
              <b-td>
                {{ local_schedule.instance_count }}
                <b-link
                  v-show="local_schedule.instance_count"
                  v-b-modal.instance_modal_id
                  :disabled="!local_schedule.instance_count"
                >
                  List
                </b-link>
                <schedule-detail-modal
                  modal-id="instance_modal_id"
                  :schedule="schedule"
                />
              </b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </b-col>
      <b-col
        lg="8"
      >
        <b-table-simple
          hover
          small
          class="text-center"
        >
          <b-thead>
            <b-tr>
              <b-th />
              <b-th>Mon</b-th>
              <b-th>Tue</b-th>
              <b-th>Wed</b-th>
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
              <b-th class="text-right">
                {{ hour }}:00
              </b-th>
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
import { Schedule } from '../store/modules/schedule'

function localScheduleFromSelected (selectedSchedule) {
  if (selectedSchedule === undefined) { return null }
  const result = _.clone(selectedSchedule)
  result.schedule = [...selectedSchedule.schedule]
  return result
}

export default {
  name: 'ScheduleDetail',
  components: {
    ScheduleDetailModal: () => import('./ScheduleDetailModal'),
    ScheduleDetailDeleteModal: () => import('./ScheduleDetailDeleteModal')
  },
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
    selectedScheduleID: { type: Number, default: undefined },
    createNew: { type: Boolean, default: false }
  },
  data: function () {
    const selectedSchedule = this.createNew ? Schedule.empty() : this.$store.getters.getScheduleById(this.selectedScheduleID)
    return {
      local_schedule: localScheduleFromSelected(selectedSchedule),
      renaming: this.createNew
    }
  },
  computed: {
    schedule: function () {
      if (this.createNew) {
        return Schedule.empty()
      } else {
        return this.$store.getters.getScheduleById(this.selectedScheduleID)
      }
    },
    isLocalModified: function () {
      return !(_.isEqual(this.local_schedule.schedule, this.schedule.schedule) && _.isEqual(this.local_schedule.active, this.schedule.active) && _.isEqual(this.local_schedule.name, this.schedule.name))
    }
  },
  watch: {
    schedule: function (newVal) {
      this.local_schedule = localScheduleFromSelected(newVal)
    },
    createNew: function (newVal) {
      this.renaming = newVal
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
    },
    deleteSchedule: function () {
      this.$emit('scheduleDelete', this.schedule)
    }
  }
}
</script>

<style scoped>
</style>
