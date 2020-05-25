<template>
  <AccordionView
    :object-list="instanceList"
    card-title="Instances"
  >
    <template v-slot:collapsedContent="slotProps">
      <InstanceAccordion
        :instance="slotProps.object"
        :schedule-list="scheduleList"
      />
    </template>
  </AccordionView>
</template>

<script>
import AccordionView from './AccordionView'
import InstanceAccordion from './InstanceAccordion'

export default {
  components: {
    AccordionView,
    InstanceAccordion
  },
  props: {
    selectedAccount: { type: Object, default: null }
  },
  computed: {
    instanceList: function () {
      const result = this.$store.state.instance.instances
      if (this.selectedAccount !== null) {
        return result.filter(instance => instance.aws_account === this.selectedAccount.url)
      }
      return result
    },
    scheduleList: function () {
      return [{ value: null, text: 'None' }, ...this.$store.state.schedule.schedules.map((schedule) => { return { value: schedule.url, text: schedule.name } })]
    }
  },
  created () {
    this.$store.dispatch('LOAD_INSTANCE_LIST').then(() => {})
    this.$store.dispatch('LOAD_SCHEDULE_LIST').then(() => {})
  }
}
</script>
