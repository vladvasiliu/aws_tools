<template>
  <div>
    {{ selectedAccount }}
  </div>
</template>

<script>
export default {
  name: 'SecurityGroupList',

  props: {
    selectedAccount: { type: Object, default: null }
  }
}
</script>

<style scoped>

</style>
