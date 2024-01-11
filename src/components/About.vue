<!-- About.vue -->
<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div>
      <h1>About Page</h1>
      <p>Page {{ pageNumber }}</p>
      <!-- Your about page content goes here -->
    </div>
  </template>
  
  <script>
  export default {
    // Component options
    props: ['pageNumber'],
    name: 'AboutPage',  // Use a multi-word name
  };
  </script>
  
  <style scoped>
  /* Component styles go here */
  </style>
  