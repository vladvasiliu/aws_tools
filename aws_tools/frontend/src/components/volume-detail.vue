<template>
  <div>
    {{ volume }}
  </div>
</template>

<script>
export default {
  name: 'VolumeDetail',
  props: {
    volume: {
      type: Object,
      default () { return {} }
    }
  }
}
</script>

<style scoped>

</style>
