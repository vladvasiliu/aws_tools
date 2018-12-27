<template>
  <div
    class="container"
    role="main">
    <div class="border-bottom mt-5 pb-3">
      <h1 class="display-4 text-center col-auto">AWS Tools</h1>
    </div>
    <h2 class="display-5 col-auto text-muted text-center mt-5 pb-4">
      <small>Login</small>
    </h2>

    <div class="row justify-content-center m-5">
      <div class="col-5">
        <b-card no-body>
          <b-tabs
            card
            no-body>
            <b-tab title="Local"> <AccountLoginLocal/> </b-tab>
            <b-tab title="SSO"> <AccountLoginSSO/> </b-tab>
          </b-tabs>
        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import AccountLoginLocal from './AccountLoginLocal'
import AccountLoginSSO from './AccountLoginSSO'

export default {
  components: {
    AccountLoginLocal,
    AccountLoginSSO
  },
  computed: {
    ...mapGetters([
      'isAuthenticated'
    ])
  }
}
</script>
