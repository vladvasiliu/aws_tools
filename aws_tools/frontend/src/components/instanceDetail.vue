<template>
  <b-card header="Details">
    <table class="table">
      <tbody>
        <tr>
          <td class="text-right border-top-0">
            ID
          </td>
          <td class="border-top-0">
            {{ instance.id }}
          </td>
        </tr>
        <tr>
          <td class="text-right">
            Region
          </td>
          <td>{{ instance.region_name }}</td>
        </tr>
        <tr>
          <td class="text-right">
            Backup
          </td>
          <td>
            <b-form-checkbox v-model="backup">
              <b-badge
                :variant="variant(instance.backup)"
                class="align-middle"
              >
                {{
                  instance.backup ? `At ${instance.backup_time}` : "Disabled"
                }}
              </b-badge>
            </b-form-checkbox>
          </td>
        </tr>
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
    variant: () => value => {
      return value ? 'success' : 'danger'
    },
    backup: {
      get () {
        return this.instance.backup
      },
      set (value) {
        let newValue = {
          instance: this.instance,
          changes: {
            backup: value
          }
        }
        this.$store.dispatch('UPDATE_INSTANCE', newValue)
      }
    }
  }
}
</script>
