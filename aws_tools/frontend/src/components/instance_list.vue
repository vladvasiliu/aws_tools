<template>
  <b-card
    header="Instances"
  >
    <b-list-group
      v-if="instanceList.length > 0"
      flush
    >
      <template v-for="instance in instanceList">
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
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'

export default {
  components: {
    instanceDetail: () => import('./instanceDetail'),
    volumeList: () => import('./volumeList')
  },
  props: {
    selectedAccount: { type: Object, default: null }
  },
  data () {
    return {
      collapseIcon: faCaretDown
    }
  },
  computed: {
    instanceList: function () {
      let result = this.$store.state.instance.instances
      if (this.selectedAccount !== null) {
        return result.filter(instance => instance.aws_account === this.selectedAccount.url)
      }
      return result
    }
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
