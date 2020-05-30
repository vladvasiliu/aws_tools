<template>
  <b-card
    no-body
  >
    <template v-slot:header>
      <strong>{{ cardTitle }}</strong>
    </template>
    <div
      v-if="objectList == null && objectError == null"
      class="text-center"
    >
      <b-spinner />
    </div>
    <div
      v-else-if="objectList == null && objectError != null"
      v-b-tooltip.hover
      class="text-center text-danger"
      :title="objectError"
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
        :to="routeDest(object)"
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
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'

export function RouteDestAll (text, location) {
  this.text = text
  this.location = location
}

export default {
  name: 'ObjectListGroupCard',
  props: {
    objectList: { type: Array, default: null },
    objectError: { type: Object, default: null },
    cardTitle: { type: String, default: 'Object list', required: true },
    routeDest: { type: Function, required: true },
    routeDestAll: { type: RouteDestAll, default: undefined, required: false }
  },
  computed: {
    faExclamationTriangle () { return faExclamationTriangle }
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
