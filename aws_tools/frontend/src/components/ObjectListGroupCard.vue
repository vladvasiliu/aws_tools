<template>
  <b-card
    no-body
  >
    <template v-slot:header>
      <b-row>
        <b-col>
          <strong>{{ cardTitle }}</strong>
        </b-col>
        <b-col
          v-if="routeDestAdd"
          cols="auto"
        >
          <b-button
            class="mt-n2 mb-n2"
            :to="routeDestAdd.location"
            variant="light"
          >
            <font-awesome-icon :icon="addIcon" />
          </b-button>
        </b-col>
      </b-row>
    </template>
    <div
      v-if="loading"
      class="text-center"
    >
      <b-spinner />
    </div>
    <div
      v-else-if="objectError"
      v-b-tooltip.hover
      class="text-center text-danger"
      :title="objectError.message"
    >
      <font-awesome-icon :icon="faExclamationTriangle" />
    </div>
    <b-list-group
      v-if="Array.isArray(objectList) && objectList.length > 0"
      flush
    >
      <b-list-group-item
        v-if="objectList.length>1 && routeDestAll"
        action
        :to="routeDestAll.location"
        active-class="active"
        exact
      >
        {{ routeDestAll.text }}
      </b-list-group-item>
      <b-list-group-item
        v-for="object in objectList"
        :key="object.id"
        action
        :to="routeDestFun(object)"
        active-class="active"
        class="text-truncate"
      >
        {{ object.name }}
      </b-list-group-item>
    </b-list-group>
    <div
      v-else-if="Array.isArray(objectList)"
      class="text-danger"
    >
      <em>None</em>
    </div>
  </b-card>
</template>

<script>
import { faExclamationTriangle, faPlus } from '@fortawesome/free-solid-svg-icons'
import { Error } from './ErrorView'

export class RouteDest {
  constructor (text, location) {
    this.text = text
    this.location = location
  }
}

export default {
  name: 'ObjectListGroupCard',
  props: {
    loading: { type: Boolean, default: true },
    objectList: { type: Array, default: null },
    objectError: { type: Error, default: null },
    cardTitle: { type: String, default: 'Object list', required: true },
    routeDestFun: { type: Function, required: true },
    routeDestAll: { type: RouteDest, default: undefined, required: false },
    routeDestAdd: { type: RouteDest, default: undefined, required: false }
  },
  computed: {
    faExclamationTriangle () { return faExclamationTriangle },
    addIcon () { return faPlus }
  }
}

</script>

<style lang="scss" scoped>
  @import "~bootstrap/scss/bootstrap";
  @import "~bootstrap-vue/dist/bootstrap-vue.css";

  .list-group-item.list-group-item-action {
    border-bottom: $border-width solid transparent;
  }

  .list-group-item.list-group-item-action.active {
    background: $light;
    color: $dark;
    border: $border-width solid transparent;
    font-weight: $font-weight-bolder;
  }
</style>
