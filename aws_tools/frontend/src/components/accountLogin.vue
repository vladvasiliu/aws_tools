<template>
  <div
    class="container"
    role="main"
  >
    <b-alert
      :show="dismissCountDown"
      dismissible
      variant="danger"
      class="fixed-top text-center w-50 mx-auto"
      @dismissed="dismissCountDown = 0;"
      @dismiss-count-down="countDownChanged"
    >
      <p>Login failed: {{ loginError }}</p>
      <b-progress
        :max="dismissSecs"
        :value="dismissCountDown"
        variant="danger"
        height="1px"
      />
    </b-alert>
    <div class="border-bottom mt-5 pt-5 pb-3">
      <h1 class="display-4 text-center col-auto">
        AWS Tools
      </h1>
    </div>
    <h2 class="display-5 col-auto text-muted text-center mt-5 pb-4">
      <small>Login</small>
    </h2>

    <div class="row justify-content-center m-5">
      <div class="col-5">
        <b-card no-body>
          <b-tabs
            card
            no-body
          >
            <b-tab title="SSO">
              <AccountLoginSSO
                @login-error="setError"
                @login-ok="redirect"
              />
            </b-tab>
            <b-tab title="Local">
              <AccountLoginLocal
                @login-error="setError"
                @login-ok="redirect"
              />
            </b-tab>
          </b-tabs>
        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
import AccountLoginLocal from './AccountLoginLocal'
import AccountLoginSSO from './AccountLoginSSO'

export default {
  components: {
    AccountLoginLocal,
    AccountLoginSSO
  },
  data: () => {
    return {
      dismissSecs: 10,
      dismissCountDown: 0,
      showDismissibleAlert: true,
      loginError: null
    }
  },
  methods: {
    countDownChanged (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    setError (error) {
      this.loginError = error
      this.dismissCountDown = this.dismissSecs
    },
    redirect () {
      this.$router.push('/')
    }
  }
}
</script>
