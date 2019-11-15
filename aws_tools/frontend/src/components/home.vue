<template>
  <div>
    Home
  </div>
</template>

<script>
import router from '../router'
export default {
  name: 'Home',
  updated () {
    router.push({ name: 'InstanceView' })
  }
}
</script>

<style scoped>

</style>
