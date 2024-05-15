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
    name: 'SearchPage',  // Updated to a multi-word name
    data() {
      return {
        users: [],
        username: "",
        searchedUser: null,
      };
    },
    methods: {
      getAllUsers() {
        // Make a request to fetch all users
        // Update the 'users' data property with the response
      },
      searchUser() {
        // Make a request to fetch user data based on the provided username
        // Update the 'searchedUser' data property with the response
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
  