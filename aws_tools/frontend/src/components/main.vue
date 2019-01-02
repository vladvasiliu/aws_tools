<template>
  <div>
    <NavBar/>

    <div class="container mt-3 mb-3">
      <div class="row">
        <div class="col-3">
          <account-list/>
        </div>
        <div class="col">
          <instance-list/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccountList from './account_list.vue'
import InstanceList from './instance_list.vue'
import NavBar from './NavBar'

export default {
  components: { AccountList, InstanceList, NavBar }
}
</script>
