<template>
  <b-card
    no-body
  >
    <template v-slot:header>
      <div class="d-flex justify-content-between align-items-center">
        <strong>{{ cardTitle }}</strong>
        <b-input-group class="w-50 search-field">
          <b-input-group-prepend>
            <b-input-group-text><font-awesome-icon :icon="searchIcon" /></b-input-group-text>
          </b-input-group-prepend>
          <b-form-input
            v-model="searchText"
            placeholder="Search..."
          />
          <b-input-group-append>
            <b-button
              v-if="searchText"
              @click="clearSearch"
            >
              <font-awesome-icon :icon="searchClearIcon" />
            </b-button>
          </b-input-group-append>
        </b-input-group>
      </div>
    </template>
    <b-list-group
      v-if="filteredObjectList.length > 0"
      flush
    >
      <template v-for="object in filteredObjectList">
        <b-list-group-item
          :key="object.id"
          v-b-toggle="object.id"
          action
          class="border-top-1 border-bottom-0 m-0 d-flex justify-content-between align-items-center object-name"
        >
          <span class="object-name-text">{{ object.name }}</span>
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
import { faCaretDown, faSearch, faTimes } from '@fortawesome/free-solid-svg-icons'

export default {
  name: 'AccordionView',
  props: {
    objectList: { type: Array, default: () => { return [] }, required: true },
    cardTitle: { type: String, default: null, required: true }
  },
  data () {
    return {
      collapseIcon: faCaretDown,
      searchIcon: faSearch,
      searchClearIcon: faTimes,
      searchText: ''
    }
  },
  computed: {
    filteredObjectList: function () {
      return this.objectList.filter(obj => obj.name.toLowerCase().includes(this.searchText.toLowerCase()) || obj.id.toLowerCase().includes(this.searchText.toLowerCase()))
    }
  },
  methods: {
    clearSearch: function () { this.searchText = '' }
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

  .object-name:not(.collapsed) {
    font-weight: bold;
  }

  .card .card-header .search-field {
    /* for header spacing */
    margin-bottom: -12px;
    margin-top: -12px;
  }
</style>
