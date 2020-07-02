import axios from 'axios'
// import { _ } from 'vue-underscore'

export class RDS {
  constructor (rds = {}) {
    this.url = rds.url
    this.aws_account = rds.aws_account
    this.name = rds.name
    this.id = this.name
    this.present = rds.present
    this.engine = rds.engine
    this.region_name = rds.region_name
    this.engine_version = rds.engine_version
    this.multi_az = rds.multi_az
    this.schedule = rds.schedule
    this.kind = rds.kind
  }
}

function compareRDS (RDSA, RDSB) {
  let compare = 0
  const nameA = RDSA.name.toUpperCase()
  const nameB = RDSB.name.toUpperCase()
  if (nameA > nameB) {
    compare = 1
  } else if (nameA < nameB) {
    compare = -1
  }
  return compare
}

export default {
  state: {
    rdsList: []
  },
  actions: {
    RDS_LOAD_LIST ({ commit }) {
      function getClusters () { return axios.get('/RDSClusters/') }
      function getInstances () { return axios.get('/RDSInstances/') }

      return new Promise((resolve, reject) =>
        Promise.all([getClusters(), getInstances()]).then(
          response => {
            commit('SET_RDS_LIST', { instanceList: response[1].data, clusterList: response[0].data })
            resolve()
          },
          err => { reject(err.toJSON()) }
        )
      )
    },
    RDS_UPDATE ({ commit }, newValue) {
      return new Promise((resolve, reject) =>
        axios.patch(newValue.url, newValue.changes).then(
          response => {
            const newRDS = new RDS(response.data)
            commit('UPDATE_RDS', { newRDS: newRDS })
            resolve(newRDS)
          },
          error => {
            reject(error.toJSON())
          }
        )
      )
    }
  },
  mutations: {
    SET_RDS_LIST: (state, { instanceList, clusterList }) => {
      const cl = clusterList.map(s => new RDS({ ...s, kind: 'cluster' }))
      const il = instanceList.map(s => new RDS({ ...s, kind: 'instance' }))
      state.rdsList = cl.concat(il).sort(compareRDS)
    },
    UPDATE_RDS: (state, { newRDS }) => {
      state.rdsList = state.rdsList.map(rds => {
        if (rds.id === newRDS.id) {
          return Object.assign(rds, newRDS)
        }
        return rds
      })
    }
  },
  getters: {
    rds: state => state.rdsList
  }
}
