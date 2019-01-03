<template>
  <b-list-group>
    <b-list-group-item
      v-for="snapshot in snapshots"
      :key="snapshot.id"
      class="d-flex justify-content-between align-items-center snapshot">
      {{ snapshot.id }}
      <span class="small font-weight-light font-italic" >
        {{ snapshot.created_at | moment("calendar") }}
        <b-button
          variant="danger"
          class="ml-2 snapshot-delete"
          size="sm"
          @click="deleteSnapshot(snapshot)">
          Delete
        </b-button>
      </span>
    </b-list-group-item>
  </b-list-group>
</template>

<script>
export default {
  name: 'VolumeDetailSnapshots',
  props: {
    snapshots: {
      type: Array,
      default () { return [] }
    }
  },
  methods: {
    deleteSnapshot (snapshot) {
      console.log(`will delete snapshot ${snapshot.id}`)
    }
  }
}
</script>

<style scoped>
.snapshot .snapshot-delete {
  display: none;
}
.snapshot:hover .snapshot-delete {
  display: inline-block;
}
</style>
