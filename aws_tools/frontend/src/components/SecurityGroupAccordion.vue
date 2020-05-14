<template>
  <div
    v-b-visible.once="setVisible"
    class="container"
  >
    <div class="row">
      <div class="col col-auto">
        <small><strong>ID:</strong> {{ securityGroup.id }}</small>
      </div>
      <div class="col col-auto">
        <small><strong>VPC:</strong> {{ securityGroup.vpc_id }}</small>
      </div>
      <div class="col col-auto">
        <small><strong>Region:</strong> {{ securityGroup.region_name }}</small>
      </div>
    </div>
    <div class="row">
      <div class="col col-auto">
        <small><strong>Description:</strong></small> {{ securityGroup.description }}
      </div>
    </div>
    <div class="row mt-3">
      <b-table-simple v-if="rules.length > 0">
        <b-thead>
          <b-tr>
            <b-th>Protocol</b-th>
            <b-th>Ports</b-th>
            <b-th colspan="2">
              Source
            </b-th>
          </b-tr>
        </b-thead>
        <b-tbody>
          <b-tr
            v-for="rule in rules"
            :key="rule.id"
          >
            <b-td>{{ rule.protocol }}</b-td>
            <b-td>{{ rule.ports }}</b-td>
            <b-td>
              <b-list-group flush>
                <b-list-group-item
                  v-for="source in rule.source"
                  :key="source.id"
                  class="m-0 p-0 bg-transparent border-0"
                >
                  {{ source.source }}
                </b-list-group-item>
              </b-list-group>
            </b-td>
          </b-tr>
        </b-tbody>
      </b-table-simple>
      <div
        v-else
        class="text-center text-danger col col-auto"
      >
        <em>No rules</em>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

const portOutput = (rule) => {
  if (rule.from_port === rule.to_port) {
    return rule.from_port
  } else {
    return rule.from_port + ' - ' + rule.to_port
  }
}

const sourceIPRangeOutput = (ipRange) => {
  return {
    source: ipRange.cidr,
    description: ipRange.description
  }
}

const sourceUserGroupPairOutput = (userGroupPair) => {
  return {
    source: userGroupPair.group_id + ' / ' + userGroupPair.user_id,
    description: userGroupPair.describe
  }
}

const sourceOutput = (rule) => {
  const result = []
  result.push(...rule.ip_range.map(sourceIPRangeOutput))
  result.push(...rule.user_group_pair.map(sourceUserGroupPairOutput))
  return result
}

const ruleForOutput = (rule) => {
  return {
    protocol: rule.ip_protocol.toUpperCase(),
    ports: portOutput(rule),
    source: sourceOutput(rule)
  }
}

export default {
  name: 'SecurityGroupAccordion',
  components: {
  },
  props: {
    securityGroup: { type: Object, default: null }
  },
  computed: {
    ...mapGetters(['securityGroupRules']),

    rules: function () {
      return this.securityGroupRules.filter(rule => rule.security_group === this.securityGroup.url).map(ruleForOutput)
    }
  },
  methods: {
    setVisible: function (isVisible) {
      if (isVisible) {
        this.$store.dispatch('getSecurityGroupRules', this.securityGroup)
      }
    }
  }
}
</script>
