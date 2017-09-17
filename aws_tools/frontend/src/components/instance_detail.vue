<template>
    <b-card header="Details">
        <table class="table">
            <tbody>
            <tr><td class="text-right">ID</td><td colspan="2">{{ instance.id }}</td></tr>
            <tr><td class="text-right">Region</td><td colspan="2">{{ instance.region_name }}</td></tr>
            </tbody>
        </table>
    </b-card>
</template>

<script>
    export default {
        props: ['instance']
    }
</script>