<template>
    <ul>
        <li v-for="instance in instance_list">
            {{ instance._name }}
        </li>
    </ul>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'

    export default {
//        computed: {
//            accounts_list: function () { return this.$store.state.aws_accounts },
//        },
        computed: mapGetters({
            instance_list: 'instances'
        }),
        created () {
            this.$store.dispatch('LOAD_INSTANCE_LIST')
        },
    }
</script>