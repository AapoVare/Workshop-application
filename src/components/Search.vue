<!-- src/views/SearchPage.vue -->
<template>
    <div id="app">
      <h1>User Management System</h1>
  
      <button @click="getAllUsers">Get All Users</button>
  
      <div>
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" />
        <button @click="searchUser">Search User</button>
      </div>
  
      <div v-if="users.length > 0">
        <h2>All Users:</h2>
        <ul>
          <li v-for="user in users" :key="user.ID">
            {{ user.Username }} - {{ user.User_created }}
          </li>
        </ul>
      </div>
  
      <div v-if="searchedUser">
        <h2>User Information:</h2>
        <ul>
          <li>ID: {{ searchedUser.ID }}</li>
          <li>Username: {{ searchedUser.Username }}</li>
          <li>User Created: {{ searchedUser.User_created }}</li>
          <li>First Name: {{ searchedUser.First_name }}</li>
          <li>Last Name: {{ searchedUser.Last_name }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['pageNumber'],
    name: 'SearchPage',
    data() {
      return {
        users: [],
        username: '',
        searchedUser: null,
      };
    },
    methods: {
      getAllUsers() {
        fetch('http://127.0.0.1:5000/api/user_data')
          .then(response => response.json())
          .then(data => {
            this.users = data;
            this.searchedUser = null;
          })
          .catch(error => console.error('Error:', error));
      },
      searchUser() {
        if (this.username.trim() === '') {
          // Handle empty username input if needed
          return;
        }
  
        fetch(`http://127.0.0.1:5000/api/user_data?username=${encodeURIComponent(this.username)}`)
          .then(response => response.json())
          .then(data => {
            if (data.length > 0) {
              this.searchedUser = data[0];
              this.users = []; // Clear all users when searching to show only the searched user
            } else {
              this.searchedUser = null;
            }
          })
          .catch(error => console.error('Error:', error));
      },
    },
  };
  </script>
  
  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  
  button {
    margin: 10px;
    padding: 10px;
  }
  </style>