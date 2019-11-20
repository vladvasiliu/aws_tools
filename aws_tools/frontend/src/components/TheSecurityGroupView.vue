<template>
  <b-card
    title="Security groups"
    border-variant="white"
    no-body
  >
    <b-card-header header-tag="nav">
      <b-nav
        card-header
        tabs
      >
        <b-nav-item
          :to="{ name: 'SecGroupByAccount' }"
          exact
          exact-active-class="active"
        >
          By account
        </b-nav-item>
        <b-nav-item
          :to="{ name: 'SecGroupBySource' }"
          exact
          exact-active-class="active"
        >
          By source
        </b-nav-item>
      </b-nav>
    </b-card-header>
    <b-card-body>
      <router-view />
    </b-card-body>
  </b-card>
</template>

<script>
export default {
  name: 'TheSecurityGroupView',
  mounted () {
    if (this.$router.currentRoute.name === 'SecurityGroupView') {
      this.$router
        .replace({ name: 'SecGroupByAccount' })
        .then(() => {})
        .catch(() => {})
    }
  }
}
</script>

<style scoped>

</style>
