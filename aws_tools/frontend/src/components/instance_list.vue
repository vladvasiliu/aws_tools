<template>
    <b-list-group>
        <b-list-group-item v-for="instance in instances_for_selected_account" :key="instance">{{ instance._name }}</b-list-group-item>
    </b-list-group>
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