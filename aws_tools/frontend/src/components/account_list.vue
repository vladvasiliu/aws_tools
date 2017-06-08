<template>
    <ul>
        <li v-for="account in accounts_list">
            {{ account.role_arn }}
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
            accounts_list: 'aws_accounts'
        }),
        created () {
            this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
        },
    }
</script>