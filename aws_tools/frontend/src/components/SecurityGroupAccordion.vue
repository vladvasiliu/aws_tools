<template>
  <div class="container">
    <div class="row">
      <div class="col col-auto">
        <small><strong>ID:</strong></small> {{ securityGroup.id }}
      </div>
      <div class="col col-auto">
        <small><strong>Region:</strong></small> {{ securityGroup.region_name }}
      </div>
    </div>
    <div class="row">
      <div class="col col-auto">
        <small><strong>Description:</strong></small> {{ securityGroup.description }}
      </div>
    </div>
    <div class="row">
    </div>
  </div>
</template>

<script>

export default {
  name: 'SecurityGroupAccordion',
  components: {
  },
  props: {
    securityGroup: { type: Object, default: null }
  }
}
</script>