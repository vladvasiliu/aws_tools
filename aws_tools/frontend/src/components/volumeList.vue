<template>
  <b-card header="Volumes">
    <b-list-group flush>
      <!--<b-list-group-item-->
      <!--v-for="volume in volumes_for_instance(instance)"-->
      <!--:key="volume.id">{{ volume._name }}</b-list-group-item>-->
    </b-list-group>
  </b-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    instance: {
      type: Object,
      default: function () {
        return {}
      }
    }
  },

  computed: {
    ...mapGetters([
      'volumes_for_instance'
    ])
  },

  mounted () {
    this.$store
      .dispatch('GET_ALL_VOLUMES')
      .then()
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>