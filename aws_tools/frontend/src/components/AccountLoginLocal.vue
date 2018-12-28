<template>
  <b-form
    v-if="show"
    @submit.prevent="login">
    <b-form-input
      id="usernameInput"
      v-model="form.username"
      type="text"
      required
      placeholder="Username"/>
    <b-form-input
      id="passwordInput"
      v-model="form.password"
      type="password"
      required
      placeholder="Password"/>
    <b-button
      type="submit"
      variant="primary">Submit</b-button>
    <b-alert
      v-if="error"
      variant="danger"
      show>
      {{ error }}
    </b-alert>
  </b-form>
</template>

<script>
export default {
  name: 'AccountLoginLocal',
  data: () => {
    return {
      form: {
        username: '',
        password: ''
      },
      error: null,
      show: true
    }
  },
  methods: {
    login () {
      this.$store
        .dispatch('login',
          {user:
              { username: this.form.username,
                password: this.form.password}})
        .then(() => {
          console.log('Logged in. Redirecting...')
          this.$router.push({name: 'Home'})
        })
        .catch((error) => {
          console.log('Login failed. Reason:\n\t' + error)
          this.error = error.message
        })
    }
  }
}
</script>

<style scoped>
</style>
