<template>
    <div>
      <h1>Create User</h1>
      <form @submit.prevent="createUser">
        <label for="username">Username:</label>
        <input v-model="formData.Username" type="text" id="username" name="username" required><br>
  
        <label for="password">Password:</label>
        <input v-model="formData.Password" type="password" id="password" name="password" required><br>
  
        <label for="firstName">First Name:</label>
        <input v-model="formData.First_name" type="text" id="firstName" name="firstName"><br>
  
        <label for="lastName">Last Name:</label>
        <input v-model="formData.Last_name" type="text" id="lastName" name="lastName"><br>
  
        <button type="submit">Create User</button>
      </form>
    </div>
  </template>
  
  <script>
  /* import HelloWorld from './components/HelloWorld.vue'
  
  export default {
    name: 'App',
    components: {
      HelloWorld
    }
  } */
  export default {
    data() {
      return {
        formData: {
          Username: '',
          Password: '',
          First_name: '',
          Last_name: '',
        },
      };
    },
    methods: {
      createUser() {
        fetch('http://127.0.0.1:5000/api/create_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.formData),
        })
          .then((response) => response.json())
          .then((data) => {
            alert(data.message || data.error);
            if (!data.error) {
              this.formData.Username = '';
              this.formData.Password = '';
              this.formData.First_name = '';
              this.formData.Last_name = '';
            }
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      },
    },
  };
  </script>
  
  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  </style>
  