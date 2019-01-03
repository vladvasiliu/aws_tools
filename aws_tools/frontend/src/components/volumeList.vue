<template>
  <b-card header="Volumes">
    <b-list-group flush>
      <b-list-group-item
        v-for="volume in instance.ebsvolume_set"
        :key="volume.id"
        action
        class="d-flex justify-content-between align-items-center"
        @click="showModal(volume)">
        {{ volume.name }}
        <span
          v-if="volume.latest_snapshot_date"
          class="small font-weight-light font-italic ml-3" >
          {{ volume.latest_snapshot_date | moment('calendar') }}
        </span>
      </b-list-group-item>
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
      <template slot="modal-title">{{ modalVolume.name }}</template>
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
      // 'volumes_for_instance'
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
