<template>
  <b-card header="Details">
    <table class="table">
      <tbody>
        <tr><td class="text-right">ID</td><td colspan="2">{{ instance.id }}</td></tr>
        <tr><td class="text-right">Region</td><td colspan="2">{{ instance.region_name }}</td></tr>
        <tr><td class="text-right">Backup</td><td colspan="2">
          <b-form-checkbox
            :id="key"
            v-model="instance.backup">
            <span v-if="instance.backup">
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
      default: function () {
      }
    }
  },
  data: function () {
    return {
      options: [
        { text: 'On', value: true },
        { text: 'Off', value: false }
      ]
    }
  }
}
</script>
