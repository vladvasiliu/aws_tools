<template>
  <b-card
    header="Instances"
  >
    <b-list-group
      v-if="Array.isArray(instances_for_selected_account) && instances_for_selected_account.length > 0"
      flush
    >
      <template v-for="instance in instances_for_selected_account">
        <b-list-group-item
          :key="instance.id"
          v-b-toggle="instance.id"
          action
          class="border-top-1 border-bottom-0 m-0 d-flex justify-content-between align-items-center instance-name"
        >
          {{ instance.name }}
          <font-awesome-icon
            :icon="collapseIcon"
            class="instance-name-caret"
          />
        </b-list-group-item>

        <b-collapse
          :id="instance.id"
          :key="instance.id + 'detail'"
          class="w-100 justify-content-left align-self-center mb-2"
        >
          <b-list-group-item class="">
            <div class="row">
              <div class="col-auto">
                <instance-detail :instance="instance" />
              </div>
              <div class="col">
                <volume-list
                  :instance="instance"
                  class="h-100"
                />
              </div>
            </div>
          </b-list-group-item>
        </b-collapse>
      </template>
    </b-list-group>
    <div
      v-else
      class="text-center text-danger"
    >
      <em>None</em>
    </div>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'

export default {
  components: {
    instanceDetail: () => import('./instanceDetail'),
    volumeList: () => import('./volumeList')
  },
  data () {
    return {
      collapseIcon: faCaretDown
    }
  },
  computed: {
    ...mapGetters(['instances_for_selected_account'])
  },
  created () {
    this.$store.dispatch('LOAD_INSTANCE_LIST').then(() => {})
  }
}
</script>

<style>
.instance-name:hover .instance-name-caret {
  opacity: inherit;
}
.instance-name .instance-name-caret {
  opacity: 0.3;
}
.instance-name.collapsed .instance-name-caret {
  transform: rotate(90deg);
}
</style>
