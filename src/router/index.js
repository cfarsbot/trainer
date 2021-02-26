import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

// Requires Authentication
import Home from '../views/Home.vue'
import Play from '../views/Play.vue'

// Store 
import user_store from '../store/user.js'
Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {requiresAuth: true},
  },
  {
    path: '/play',
    name: 'Play',
    component: Play,
    meta: {requiresAuth: true}
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


router.beforeEach((to, from, next) => {
  console.log(to);
  if (to.matched.some(record => record.meta.requiresAuth)) {

    // TODO: Check the Token if it is valid, before redirect
    // TODO: Encrypt user id with JWT on Serverside
    var user = user_store.getters.user;
    console.log(user.id)
  
    if ( user.id === undefined) {
      console.log("user not found")
      next({ name: 'Login' })
      
    } else {
      next()
    }
  } else {
    next() 
  }
})




export default router
