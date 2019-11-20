<template>
  <div v-if="!api_status.busy && !api_status.error">
    {{ securityGroupList }}
  </div>
  <loading v-else />
</template>

<script>
import { mapGetters } from 'vuex'
import Loading from './loading'

export default {
  name: 'SecurityGroupList',

  components: {
    Loading
  },

  props: {
    selectedAccount: { type: Object, default: null }
  },

  data () {
    return {
      api_status: {
        busy: true,
        error: false
      }
    }
  },

  computed: {
    ...mapGetters(['securityGroupList']),
    filteredSecurityGroupList: function () {
      let result = this.securityGroupList
      if (this.selectedAccount !== null) {
        result = result.filter(securityGroup => securityGroup.aws_account === this.selectedAccount.url)
      }
      return result
    }
  },

  mounted () {
    this.$store.dispatch('getSecurityGroupList')
      .then(() => { this.api_status.busy = false })
      .catch(error => {
        this.api_status.busy = false
        this.api_status.error = error
      })
  }
}
</script>

<style scoped>

</style>
