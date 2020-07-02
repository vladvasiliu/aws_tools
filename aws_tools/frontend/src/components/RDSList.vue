<template>
  <AccordionView
    :object-list="rdsList"
    card-title="Databases"
  >
    <template v-slot:collapsedContent="slotProps">
      <RDSAccordion
        :instance="slotProps.object"
      />
    </template>
  </AccordionView>
</template>

<script>
import AccordionView from './AccordionView'
import RDSAccordion from './RDSAccordion'
export default {
  name: 'RDSList',
  components: { RDSAccordion, AccordionView },
  props: {
    selectedAccountID: { type: String, default: undefined, required: false },
    error: { type: String, default: '', required: false }
  },
  computed: {
    rdsList: function () {
      const result = this.$store.state.rds.rds

      if (this.selectedAccountID !== undefined) {
        return result.filter(rds => rds.aws_account === this.selectedAccountID)
      } else {
        return result
      }
    }
  }
}
</script>

<style scoped>

</style>
