<template>
  <b-container>
    <b-row
      cols-sm="1"
      cols-xl="3"
    >
      <b-col sm="auto">
        <strong>ID: </strong>{{ instance.id }}
      </b-col>
      <b-col sm="auto">
        <strong>Region: </strong>{{ instance.region_name }}
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="3">
        <strong>Backup: </strong>
      </b-col>
      <b-col cols="9">
        <b-form-checkbox
          v-model="backup"
          inline
          switch
        >
          <b-badge
            :variant="variant(instance.backup)"
            class="align-middle"
          >
            {{ instance.backup ? `At ${instance.backup_time}` : "Disabled" }}
          </b-badge>
        </b-form-checkbox>
      </b-col>
      <b-col
        cols="3"
        align-self="center"
      >
        <strong>Schedule:</strong>
      </b-col>
      <b-col cols="9">
        <b-select
          v-model="schedule"
          :options="scheduleList"
          inline
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  props: {
    instance: { type: Object, required: true },
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
