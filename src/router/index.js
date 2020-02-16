import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Setup from '../views/Setup.vue'
import ParkingEnter from '../views/ParkingEnter.vue'
import ParkingExit from '../views/ParkingExit.vue'
import OTP from '../views/reqOTP.vue'
import VIP from '../views/VIP.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'home',
    component: Home
  },
  {
    path: '/',
    name: 'login',
    component: Login
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
  },
  {
    path: '/setup',
    name: 'setup',
    component: Setup
  },
  
  {
    path: '/enterParking/parkingExit',
    name: 'parkingExit',
    component: ParkingExit
  },
  {
    path: '/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/enterParking/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/enterParking/enterParking/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/enterParking/enterParking/enterParking/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/enterParking/enterParking/enterParking/enterParking/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/enterParking/enterParking/enterParking/enterParking/enterParking/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/enterParking/enterParking/enterParking/enterParking/enterParking/enterParking/enterParking/:parkingLot',
    name: 'parkingEnter',
    component: ParkingEnter
  },
  {
    path: '/otp',
    name: 'otp',
    component: OTP
  },
  {
    path: '/vip',
    name: 'vip',
    component: VIP
  }
  
]

const router = new VueRouter({
  routes
})

export default router
