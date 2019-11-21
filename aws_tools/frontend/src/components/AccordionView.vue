<template>
  <b-card
    header="Instances"
  >
    <b-list-group
      v-if="objectList.length > 0"
      flush
    >
      <template v-for="object in objectList">
        <b-list-group-item
          :key="object.id"
          v-b-toggle="object.id"
          action
          class="border-top-1 border-bottom-0 m-0 d-flex justify-content-between align-items-center object-name"
        >
          {{ object.name }}
          <font-awesome-icon
            :icon="collapseIcon"
            class="object-name-caret"
          />
        </b-list-group-item>

        <b-collapse
          :id="object.id"
          :key="object.id + 'detail'"
          class="w-100 justify-content-left align-self-center mb-2"
        >
          <b-list-group-item class="">
            <slot
              name="collapsedContent"
              :object="object"
            />
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
  name: 'AccordionView',
  props: {
    objectList: { type: Array, default: () => { return [] } }
  },
  data () {
    return {
      collapseIcon: faCaretDown
    }
  }
}
</script>

<style>
  .object-name:hover .object-name-caret {
    opacity: inherit;
  }

  .object-name .object-name-caret {
    opacity: 0.3;
  }

  .object-name.collapsed .object-name-caret {
    transform: rotate(90deg);
  }
</style>
