<!-- src/views/Home.vue -->
<!-- eslint-disable vue/multi-word-component-names -->

<template>
    <div>
      <h2>Home Page</h2>
      <p>Page {{ pageNumber }}</p>
      <!-- Your home page content -->
    </div>
  </template>
  
  <script>
  export default {
    // Component options
    props: ['pageNumber'],
    name: 'HomePage',  // Use a multi-word name
  };
  </script>