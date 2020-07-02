<template>
  <AccordionView
    :object-list="instanceList"
    card-title="Instances"
  >
    <template v-slot:collapsedContent="slotProps">
      <InstanceAccordion
        :instance="slotProps.object"
        :schedule-list="scheduleSelectOptions"
      />
    </template>
  </AccordionView>
</template>

<script>
import AccordionView from './AccordionView'
import InstanceAccordion from './InstanceAccordion'
import { mapGetters } from 'vuex'

export default {
  components: {
    AccordionView,
    InstanceAccordion
  },
  props: {
    selectedAccountID: { type: String, default: undefined, required: false }
  },
  computed: {
    instanceList: function () {
      const result = this.$store.state.instance.instances
      if (this.selectedAccountID !== undefined) {
        return result.filter(instance => instance.aws_account === this.selectedAccountID)
      }
      return result
    },
    ...mapGetters(['scheduleSelectOptions'])
  },
  created () {
    this.$store.dispatch('LOAD_INSTANCE_LIST').then(() => {})
    this.$store.dispatch('SCHEDULE_LOAD_LIST').then(() => {})
  }
}
</script>
