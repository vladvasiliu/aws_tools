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
                        <b-card header="Details" class="m-1">
                            <table class="table">
                                <tbody>
                                    <tr><td class="text-right">ID</td><td colspan="2">{{ instance.id }}</td></tr>
                                    <tr><td class="text-right">Region</td><td colspan="2">{{ instance.region_name }}</td></tr>
                                    <tr><td class="text-right">Backup</td><td>{{ instance.backup_time }}</td><td><b-form-radio v-model="instance.backup" :options="[true, false]" stacked></b-form-radio></td></tr>
                                </tbody>
                            </table>
                        </b-card>
                        <b-card header="Volumes" class="m-1"></b-card>
                    </div>
                </b-collapse>
            </b-list-group-item>
        </b-list-group>
    </b-card>
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