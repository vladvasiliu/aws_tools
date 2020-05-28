<template>
  <b-container class="text-center">
    <b-row>
      <b-col>
        <h1 class="display-4 border-bottom m-5 mb-0 pb-3">
          {{ title }}
        </h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        {{ message }}
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'NothingSelected',
  props: {
    title: { type: String, default: 'No object selected' },
    message: { type: String, default: 'Please select an object' }
  }
}
</script>

<style scoped>

</style>
