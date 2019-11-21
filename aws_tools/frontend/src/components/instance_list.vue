<template>
  <AccordionView :object-list="instanceList" />
</template>

<script>
import AccordionView from './AccordionView'

export default {
  components: {
    AccordionView
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
