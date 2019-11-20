<template>
  <div>
    {{ securityGroupList }}
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'SecurityGroupList',

  props: {
    selectedAccount: { type: Object, default: null }
  },

  computed: {
    ...mapGetters(['securityGroupList'])
  },

  mounted () {
    this.$store.dispatch('getSecurityGroupList')
  }
}
</script>

<style scoped>

</style>
