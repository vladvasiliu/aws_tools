<template>
  <div class="row">
    {{ securityGroup.url }}
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
