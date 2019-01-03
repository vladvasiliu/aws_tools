<template>
  <b-card header="Volumes">
    <b-list-group flush>
      <b-list-group-item
        v-for="volume in volumes_for_instance(instance)"
        :key="volume.id"
        action
        @click="showModal(volume)">{{ volume_name(volume) }}</b-list-group-item>
    </b-list-group>
    <b-modal
      v-if="modalShow"
      v-model="modalShow"
      ok-title="Close"
      size="lg"
      hide-footer
      header-bg-variant="light"
      ok-only
      lazy
      centered>
      <template slot="modal-title">{{ volume_name(modalVolume) }}</template>
      <volume-detail
        :volume="modalVolume"
        :instance="instance" />
    </b-modal>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  components: {
    'volume-detail': () => import('./volume-detail')
  },
  props: {
    instance: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      modalVolume: null
    }
  },
  computed: {
    ...mapGetters([
      'volumes_for_instance',
      'volume_name'
    ]),
    modalShow: {
      get () { return !!this.modalVolume },
      set (value) {
        if (!value) {
          this.modalVolume = null
        }
      }
    }
  },
  methods: {
    showModal (volume) {
      this.modalVolume = volume
    }
  }
}
</script>
