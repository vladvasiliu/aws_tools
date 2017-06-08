<template>
    <div>
        <account-list></account-list>
        <!--<br/>-->
        <!--<instance-list></instance-list>-->
    </div>
</template>

<script>
    import AccountList from './account_list.vue'
    import InstanceList from './instance_list.vue'

    export default {
        components: { AccountList, InstanceList }
    }
</script>