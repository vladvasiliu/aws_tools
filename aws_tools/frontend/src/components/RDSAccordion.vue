<template>
  <b-container>
    <b-row>
      {{ instance.name }}
    </b-row>
  </b-container>
</template>

<script>
import { RDS } from '../store/modules/rds'

export default {
  name: 'RDSAccordion',
  props: {
    instance: { type: RDS, required: true }
  }
}
</script>

<style scoped>

</style>
