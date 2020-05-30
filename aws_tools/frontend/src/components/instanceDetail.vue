<template>
  <b-container>
    <b-row
      cols-sm="1"
      cols-xl="3"
      class="border-bottom"
    >
      <b-col sm="auto">
        <strong>ID: </strong>{{ instance.id }}
      </b-col>
      <b-col sm="auto">
        <strong>Region: </strong>{{ instance.region_name }}
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-form-group
          label="Backup"
          label-class="font-weight-bold"
          label-cols="2"
          :label-for="'backup-checkbox-' + instance.id"
        >
          <b-form-checkbox
            :id="'backup-checkbox-' + instance.id"
            v-model="backup"
            switch
            inline
          >
            <b-badge
              :variant="variant(instance.backup)"
            >
              {{ instance.backup ? `At ${instance.backup_time}` : "Disabled" }}
            </b-badge>
          </b-form-checkbox>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-form-group
          label="Schedule"
          label-cols="2"
          label-class="font-weight-bold"
        >
          <b-input-group>
            <b-select
              v-model="schedule"
              :options="scheduleList"
              inline
            />
            <b-input-group-append v-if="schedule">
              <b-button :to="{ name: 'ScheduleViewID', params: { id: schedule } }" variant="info">
                Show
              </b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form-group>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { Instance } from '../store/modules/instance'

export default {
  props: {
    instance: { type: Instance, required: true },
    scheduleList: { type: Array, required: true }
  },
  computed: {
    variant: () => value => {
      return value ? 'success' : 'danger'
    },
    backup: {
      get () {
        return this.instance.backup
      },
      set (value) {
        const newValue = {
          instance: this.instance,
          changes: {
            backup: value
          }
        }
        this.$store.dispatch('UPDATE_INSTANCE', newValue)
      }
    },
    schedule: {
      get () {
        return this.instance.schedule
      },
      set (value) {
        const newValue = {
          instance: this.instance,
          changes: {
            schedule: value
          }
        }
        this.$store.dispatch('UPDATE_INSTANCE', newValue)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  @media (min-width: 576px) {
    div.custom-control.custom-control-inline.custom-switch {
      /* Comment the following line to see the original BS4 css without the hack */
      padding-top: calc(.375rem + 1px); /* col-form-label padding */
    }
  }
</style>
