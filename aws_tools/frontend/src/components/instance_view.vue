<template>
  <div class="row">
    <div class="col-3">
      <account-list />
    </div>
    <div class="col">
      <instance-list />
    </div>
  </div>
</template>

<script>
import AccountList from './account_list.vue'
import InstanceList from './instance_list.vue'

export default {
  components: { AccountList, InstanceList }
}
</script>
