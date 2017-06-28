<template>
    <div id="app">
        <b-navbar toggleable type="inverse sticky-top" class="bg-inverse">
    
            <b-link class="navbar-brand" to="#">
                <span>AWS Tools</span>
            </b-link>
    
    <!--
            <b-collapse is-nav id="nav_collapse">
                <b-nav is-nav-bar>
                    <b-nav-item>Instances</b-nav-item>
                </b-nav>
            </b-collapse>

     -->
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
    import ElRow from "element-ui/packages/row/src/row";

    export default {
        components: {
            ElRow,
            AccountList, InstanceList }
    }
</script>
