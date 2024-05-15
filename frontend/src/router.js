// src/router.js
import { createRouter, createWebHistory } from 'vue-router';

// Import your components for each page
//import Home from './views/Home.vue';
import Search from './views/Search.vue';
//import Contact from './views/Contact.vue';

const routes = [
  //{ path: '/', component: Home },
  { path: '/search', component: Search },
  //{ path: '/contact', component: Contact },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
