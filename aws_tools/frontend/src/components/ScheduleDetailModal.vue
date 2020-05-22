<template>
  <b-modal
    :id="modalId"
    :title="schedule.name"
    centered
    scrollable
    hide-footer
    header-bg-variant="light"
    header-text-variant="dark"
    title-class="font-weight-bold"
    size="lg"
    @shown="getData"
    @hidden="clearData"
  >
    <Loading
      v-if="loading"
      message="Loading instances..."
    />
    <Error
      v-else-if="error"
      :message="error.message"
    />
    <AccordionView
      v-else
      card-title="Instances"
      :object-list="instance_list"
    >
      <template v-slot:collapsedContent="slotProps">
        <b-list-group flush>
          <b-list-group-item
            v-for="instance in slotProps.object.instance_set"
            :key="instance.id"
          >
            {{ instance.name }}
          </b-list-group-item>
        </b-list-group>
      </template>
    </AccordionView>
  </b-modal>
</template>

<script>
import AccordionView from './AccordionView'
export default {
  name: 'ScheduleDetailModal',
  components: {
    AccordionView,
    Error: () => import('./error'),
    Loading: () => import('./loading')
  },
  props: {
    schedule: { type: Object, required: true },
    modalId: { type: String, required: true }
  },
  data () {
    return {
      instance_list: [],
      loading: true,
      error: null
    }
  },
  methods: {
    getData: function () {
      this.axios
        .get(this.schedule.instance_list)
        .then(response => {
          console.log(response.data)
          this.instance_list = response.data
          if (!this.instance_list.length) {
            this.error = { message: 'No instances found.' }
          }
        })
        .catch(error => {
          if (!error.response) {
            this.error = error
          } else {
            this.error = { message: error.response.statusText }
          }
        })
        .finally(() => {
          this.loading = false
        })
    },
    clearData: function () {
      this.instance_list = []
      this.loading = true
      this.error = null
    }
  }
}
</script>

<style scoped>

</style>
