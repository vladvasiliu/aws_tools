<template>
  <div class="list-group list-group-flush justify-content-between">
    <div
      class="list-group-item list-group-item-action"
      @click="socialLogin"> AzureAD </div>
  </div>
</template>

<script>
export default {
  name: 'AccountLoginSSO',
  methods: {
    socialLogin () {
      this.$store.dispatch('socialLogin')
        .then(() => { this.$emit('login-ok') })
        .catch((error) => {
          console.log('Login failed. Reason:\n\t' + error)
          this.$emit('login-error', error.message)
        })
    }
  }
}
</script>

<style scoped>
</style>
