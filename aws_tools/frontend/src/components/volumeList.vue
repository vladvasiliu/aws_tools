<template>
  <b-card header="Volumes">
    <b-list-group
      v-if="instance.ebsvolume_set.length > 0"
      flush
    >
      <b-list-group-item
        v-for="volume in instance.ebsvolume_set"
        :key="volume.id"
        class="d-flex justify-content-between align-items-center volume"
      >
        {{ volume.name }}
        <div class="small font-weight-light font-italic ml-3 snapshot">
          <div class="non-hover">
            <span v-if="volume.latest_snapshot_date">
              {{ volume.latest_snapshot_date | moment("calendar") }}
            </span>
            <span v-else>
              No snapshots
            </span>
          </div>
          <div class="on-hover">
            <b-link
              v-b-tooltip.hover.left
              title="Create snapshot"
              class="ml-2 mr-2 text-primary create-snapshot"
              href="#"
              @click.prevent="createSnapshot(volume)"
            >
              <font-awesome-icon :icon="snapshotIcon" />
            </b-link>
            <span
              v-b-tooltip.hover.right
              :title="volume.latest_snapshot_date ? 'Show snapshots' : 'No snapshots'"
              class="ml-2 p-0"
            >
              <b-link
                class="text-info"
                :class="volume.latest_snapshot_date ? 'text-info' : 'text-muted'"
                :disabled="!volume.latest_snapshot_date"
                href="#"
                @click.prevent="showModal(volume)"
              >
                <font-awesome-icon :icon="infoIcon" />
              </b-link>
            </span>
          </div>
        </div>
      </b-list-group-item>
    </b-list-group>
    <div
      v-else
      class="text-center text-danger"
    >
      <em>None</em>
    </div>
    <b-modal
      v-if="modalShow"
      v-model="modalShow"
      ok-title="Close"
      size="lg"
      hide-footer
      header-bg-variant="light"
      ok-only
      lazy
      centered
    >
      <template slot="modal-title">
        {{ modalVolume.name }}
      </template>
      <volume-detail
        :volume="modalVolume"
        :instance="instance"
      />
    </b-modal>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'
import { faInfoCircle, faDownload } from '@fortawesome/free-solid-svg-icons'

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
      modalVolume: null,
      infoIcon: faInfoCircle,
      snapshotIcon: faDownload
    }
  },
  computed: {
    ...mapGetters([
      // 'volumes_for_instance'
    ]),
    modalShow: {
      get () {
        return !!this.modalVolume
      },
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
    },
    createSnapshot (volume) {
      this.axios.post(volume.url + 'create_snapshot/')
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
  .volume:hover .on-hover {
    display: inline-block;
  }
  .volume:hover .non-hover {
    display: none;
  }
  .volume:hover a.disabled {
    pointer-events: none;
  }
  .volume .on-hover {
    display: none;
  }
  .volume .non-hover {
    display: inline-block;
  }
</style>
