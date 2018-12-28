<template>
  <b-form
    v-if="show"
    @submit.prevent="login">
    <label
      id="usernameGroup"
      for="usernameInput"
      class="sr-only"/>
    <b-form-input
      id="usernameInput"
      v-model="form.username"
      type="text"
      required
      placeholder="Username"/>
    <label
      id="passwordGroup"
      for="passwordInput"
      class="sr-only"/>
    <b-form-input
      id="passwordInput"
      v-model="form.password"
      type="password"
      title="password"
      required
      placeholder="Password"
      class="mt-1"/>
    <b-button
      type="submit"
      variant="primary"
      class="mt-3 w-100">Submit</b-button>
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
          this.$emit('login-error', error.message)
        })
    }
  }
}
</script>

<style scoped>
</style>
