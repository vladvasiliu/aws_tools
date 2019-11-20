<template>
  <b-card :header="cardTitle">
    <b-list-group
      v-if="objectList.length > 0"
      flush
    >
      <template v-for="object in objectList">
        <b-list-group-item
          :key="object.id"
          v-b-toggle="object.id"
          action
          class="border-top-1 border-bottom-0 m-0 d-flex justify-content-between align-items-center instance-name"
        >
          {{ object._name }}
        </b-list-group-item>
      </template>
    </b-list-group>
  </b-card>
</template>

<script>
export default {
  name: 'AccordionListView',

  props: {
    objectList: { type: Array, default: () => { return [] } },
    cardTitle: { type: String, default: () => { return 'Undefined title' } }
  }
}
</script>

<style scoped>

</style>
