<template>
    <div>
        <ul>
            <li v-on:click="select()">
                All
                <span v-if="!account_selected"> <-- Selected</span>
            </li>
            <li v-for="account in accounts_list" v-on:click="select(account)">
                {{ account._name }}
                <span v-if="account == account_selected"> <- SELECTED</span>
            </li>
        </ul>
    </div>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'

    export default {
//        computed: {
//            accounts_list: function () { return this.$store.state.aws_accounts },
//        },
        computed: mapGetters({
            accounts_list: 'aws_accounts',
            account_selected: 'aws_account_selected'
        }),
        created () {
            this.$store.dispatch('LOAD_AWS_ACCOUNT_LIST')
        },
        methods: {
            select: function(account) {
                if (account) {
                    this.$store.commit('SET_SELECTED_ACCOUNT', {account: account})
                } else {
                    this.$store.commit('SET_SELECTED_ACCOUNT', {account: null})
                }
            }
        }
    }
</script>