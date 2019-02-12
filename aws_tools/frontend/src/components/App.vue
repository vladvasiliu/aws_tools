<template>
    <div id="app">
        <b-navbar type="dark" variant="dark">

            <b-navbar-brand>
                <span>AWS Tools</span>
            </b-navbar-brand>

        </b-navbar>

        <div class="container-fluid mt-3">
            <div class="row">
                <div class="col-2">
                    <account-list></account-list>
                </div>
                <div class="col">
                    <instance-list></instance-list>
                </div>
            </div>
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
