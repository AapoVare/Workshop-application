<!-- Login.vue -->
<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
  
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
  
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: process.env.VUE_APP_PASSWORD || '', // Fetch password from .env
      };
    },
    methods: {
      async login() {
        try {
          const loginData = {
            username: this.username,
            password: this.password,
          };
  
          const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData),
          });
  
          if (response.ok) {
            // Authentication successful, you can handle the response accordingly
            console.log('Login successful');
          } else {
            // Authentication failed, handle errors
            console.error('Login failed');
          }
        } catch (error) {
          console.error('Error during login:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Component styles go here */
  </style>
  