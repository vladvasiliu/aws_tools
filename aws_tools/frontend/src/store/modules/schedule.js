import axios from 'axios'

export class Schedule {
  constructor (schedule = {}) {
    this.url = schedule.url
    this.id = schedule.id
    this.instance_count = schedule.instance_count
    this.instance_list = schedule.instance_list
    this.name = schedule.name
    this.schedule = schedule.schedule
    this.active = schedule.active
  }
}

export default {
  state: {
    schedules: [],
    schedules_error: null
  },
  actions: {
    LOAD_SCHEDULE_LIST ({ commit }) {
      axios.get('/Schedules/').then(
        response => {
          commit('SET_SCHEDULE_LIST', { list: response.data })
        },
        err => {
          console.error(err)
          commit('SET_SCHEDULE_ERROR', { error: err })
        }
      )
    },
    UPDATE_SCHEDULE ({ commit }, newValue) {
      axios.patch(newValue.schedule.url, newValue.changes).then(response => {
        commit('UPDATE_SCHEDULE', { newSchedule: response.data })
      })
    }
  },
  mutations: {
    SET_SCHEDULE_LIST: (state, { list }) => {
      state.schedules = list.map(s => new Schedule(s))
    },
    SET_SCHEDULE_ERROR: (state, { error }) => {
      state.schedules_error = error.message
    },
    UPDATE_SCHEDULE: (state, { newSchedule }) => {
      state.schedules = state.schedules.map(schedule => {
        if (schedule.url === newSchedule.url) {
          return Object.assign(schedule, newSchedule)
        }
        return schedule
      })
    }
  },
  getters: {
    schedules: state => state.schedules,
    schedules_error: state => state.schedules_error,
    getScheduleById: (state) => (id) => {
      return state.schedules.find(schedule => schedule.id === id)
    }
  }
}
