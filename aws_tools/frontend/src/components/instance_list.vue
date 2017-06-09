<template>
    <ul>
        <li v-for="instance in instances_for_selected_account">
            {{ instance._name }}
        </li>
    </ul>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'

    export default {
        computed: {
            ...mapGetters([
                'instances_for_selected_account',
            ]),
        },
        created () {
            this.$store.dispatch('LOAD_INSTANCE_LIST')
        },
    }
</script>