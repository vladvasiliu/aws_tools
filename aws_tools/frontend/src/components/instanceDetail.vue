<template>
  <b-card header="Details">
    <table class="table">
      <tbody>
        <tr><td class="text-right">ID</td><td colspan="2">{{ instance.id }}</td></tr>
        <tr><td class="text-right">Region</td><td colspan="2">{{ instance.region_name }}</td></tr>
        <tr><td class="text-right">Backup</td><td colspan="2">
          <b-form-checkbox
            v-model="backup">
            <span v-if="backup">
              <b-badge variant="success">
                At {{ instance.backup_time }}
              </b-badge>
            </span>
            <span v-else>
              <b-badge variant="danger">
                Disabled
              </b-badge>
            </span>
          </b-form-checkbox>
        </td></tr>
      </tbody>
    </table>
  </b-card>
</template>

<script>

export default {
  props: {
    instance: {
      type: Object,
      default: function () {}
    }
  },
  computed: {
    backup: {
      get () {
        return this.instance.backup
      },
      set (value) {
        let newValue = {
          instance: this.instance,
          changes: {
            'backup': value
          }
        }
        this.$store.dispatch('UPDATE_INSTANCE', newValue)
      }
    }
  }
}
</script>
