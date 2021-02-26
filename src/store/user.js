import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {}
  },

mutations: {
        saveUser(state, payload) {
            state.user = payload;
        }
  },
  actions: {
  },
  modules: {
  },
  getters:{
    user(state){
      return state.user
    }
  }
})
