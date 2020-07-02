<template>
  <b-container>
    <b-row>
      <b-col cols="auto">
        <b-table-simple
          borderless
          small
        >
          <b-tbody>
            <b-tr class="h-100">
              <b-th>Region</b-th>
              <b-td>
                {{ instance.region_name }}
                <b-badge :variant="instance.multi_az ? 'primary' : 'secondary'">
                  {{ instance.multi_az ? 'Multi-AZ' : 'Single AZ' }}
                </b-badge>
              </b-td>
            </b-tr>
            <b-tr class="h-100">
              <b-th>Engine</b-th>
              <b-td>{{ instance.engine }} {{ instance.engine_version }}</b-td>
            </b-tr>
            <b-tr>
              <b-th class="align-middle">
                Schedule
              </b-th>
              <b-td>
                <b-input-group size="sm">
                  <b-select
                    v-model="schedule"
                    :options="scheduleList"
                    inline
                    small
                  />
                  <b-input-group-append v-if="schedule">
                    <b-button
                      :to="{ name: 'ScheduleViewID', params: { id: schedule } }"
                      variant="info"
                    >
                      Show
                    </b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-td>
            </b-tr>
          </b-tbody>
        </b-table-simple>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { RDS } from '../store/modules/rds'

export default {
  name: 'RDSAccordion',
  props: {
    instance: { type: RDS, required: true },
    scheduleList: { type: Array, required: true }
  },
  computed: {
    schedule: {
      get () { return this.instance.schedule },
      set (value) {
        const newRDS = {
          url: this.instance.url,
          changes: {
            schedule: value
          }
        }
        this.$store.dispatch('RDS_UPDATE', newRDS).then(
          () => {},
          err => {
            const h = this.$createElement
            const message = h(
              'p',
              {},
              [
                h('strong', {}, 'Cluster not found: ' + this.instance.name),
                h('p', {}, ''),
                h('em', {}, err.message)
              ]
            )
            this.$bvToast.toast([message], {
              title: 'Failed to set schedule',
              solid: true,
              variant: 'danger'
            })
          }
        )
      }
    }
  }
}
</script>

<style scoped>

</style>
