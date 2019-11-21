<template>
  <AccordionView
    :object-list="instanceList"
    card-title="Instances"
  >
    <template v-slot:collapsedContent="slotProps">
      <InstanceAccordion :instance="slotProps.object" />
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
    }
  },
  created () {
    this.$store.dispatch('LOAD_INSTANCE_LIST').then(() => {})
  }
}
</script>
