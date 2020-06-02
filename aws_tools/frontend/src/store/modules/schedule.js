import axios from 'axios'
import { _ } from 'vue-underscore'

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

  static empty () {
    return new Schedule({
      name: 'New Schedule',
      schedule: _.range(24 * 7).map(() => 0),
      active: true
    })
  }
}

function compareSchedule (scheduleA, scheduleB) {
  let compare = 0
  const nameA = scheduleA.name.toUpperCase()
  const nameB = scheduleB.name.toUpperCase()
  if (nameA > nameB) {
    compare = 1
  } else if (nameA < nameB) {
    compare = -1
  }
  return compare
}

export default {
  state: {
    schedules: [],
    schedules_error: null
  },
  actions: {
    SCHEDULE_LOAD_LIST ({ commit }) {
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
    SCHEDULE_UPDATE ({ commit }, newValue) {
      let action
      if (newValue.schedule.url) {
        action = axios.patch(newValue.schedule.url, newValue.changes)
      } else {
        action = axios.post('/Schedules/', newValue.schedule)
      }

      return new Promise((resolve, reject) =>
        action.then(
          response => {
            const newSchedule = new Schedule(response.data)
            commit('UPDATE_SCHEDULE', { newSchedule: newSchedule })
            resolve(newSchedule)
          },
          error => {
            reject(error.toJSON())
          }
        )
      )
    },
    SCHEDULE_DELETE ({ commit }, schedule) {
      return new Promise((resolve, reject) =>
        axios.delete(schedule.url).then(
          () => {
            commit('DELETE_SCHEDULE', { schedule })
            resolve()
          },
          error => {
            reject(error.toJSON())
          }
        )
      )
    }
  },
  mutations: {
    SET_SCHEDULE_LIST: (state, { list }) => {
      state.schedules = list.map(s => new Schedule(s)).sort(compareSchedule)
    },
    SET_SCHEDULE_ERROR: (state, { error }) => {
      state.schedules_error = error.message
    },
    UPDATE_SCHEDULE: (state, { newSchedule }) => {
      const oldSchedule = state.schedules.find(schedule => schedule.id === newSchedule.id)
      if (oldSchedule) {
        Object.assign(oldSchedule, newSchedule)
      } else {
        state.schedules.push(newSchedule)
      }
      state.schedules = state.schedules.sort(compareSchedule)
    },
    DELETE_SCHEDULE: (state, { schedule }) => {
      const scheduleIdx = state.schedules.findIndex(obj => obj.id === schedule.id)
      state.schedules.splice(scheduleIdx, 1)
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
