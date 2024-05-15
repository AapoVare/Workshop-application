<!-- App.vue -->
<template>
  <div>
    <button @click="navigateToPreviousPage" :disabled="currentPage === 1">Previous</button>
    <button @click="navigateToNextPage" :disabled="currentPage === totalPages">Next</button>
    <!-- <RadioQuestions :questions="questions" @submit="handleSubmission" /> -->

    <component :is="currentPageComponent" :pageNumber="currentPage"></component>
  </div>
</template>

<script>
import DOMPurify from 'dompurify';
import Home from './components/Home.vue';
import About from './components/About.vue';
import Search from './components/Search.vue';
import CreateUser from './components/CreateUser.vue'
import RadioQuestions from "./components/RadioQuestions.vue";
import Checkbox from './components/Checkbox.vue'
import SearchAnswers from './components/SearchAnswers.vue'
import Login from './components/Login.vue';
import PieChart from './components/Piechart.vue';
import ShortText from './components/ShortText.vue';
import QuestionAnswers from './components/Answers.vue';

export default {
  data() {
    return {
      currentPage: 1,
      totalPages: 11, // Adjust based on the total number of pages
    };
  },
  computed: {
    currentPageComponent() {
      switch (this.currentPage) {
        case 1:
          return Home;
        case 2:
          return CreateUser;
        case 3:
          return Login;
        case 4:
          return Search;
        case 5:
          return RadioQuestions;
        case 6:
          return Checkbox;
        case 7:
          return SearchAnswers;
        case 8:
          return About;
        case 9:
          return PieChart;
        case 10:
          return ShortText;
        case 11:
          return QuestionAnswers;
        default:
          return Home;
      }
    },
  },
  methods: {
    navigateToPreviousPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    navigateToNextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
  },
  mounted() {
    // Example of sanitizing dynamic content using Dompurify
    this.currentPageComponent = DOMPurify.sanitize(this.currentPageComponent);
  }
};
</script>

<style scoped>
/* Component styles go here */
</style>