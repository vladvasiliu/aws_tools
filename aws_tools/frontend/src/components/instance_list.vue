<template>
    <b-card header="Instances">
        <b-list-group flush>
            <b-list-group-item action
                               v-for="instance in instances_for_selected_account"
                               :key="instance.id"
                               v-b-toggle="instance.id"
                               class="flex-column align-items-start"
                               @click.self>
                {{ instance._name }}
                <b-collapse :id="instance.id" class="w-100 align-self-center">
                    <div class="d-flex m-3 justify-content-left" @click.stop>
                        <instance_detail class="m-1" :instance="instance"></instance_detail>
                        <volume_list class="m-1"></volume_list>
                    </div>
                </b-collapse>
            </b-list-group-item>
        </b-list-group>
    </b-card>
</template>

<script>
    import { mapGetters, mapActions } from 'vuex'

    import volume_list from './volume_list.vue'
    import instance_detail from './instance_detail.vue'

    export default {
        computed: {
            ...mapGetters([
                'instances_for_selected_account',
            ]),
        },
        created () {
            this.$store.dispatch('LOAD_INSTANCE_LIST')
        },
        components: {
            volume_list, instance_detail
        }
    }
</script>