<template>
  <div>
    <input v-model="searchUsername" placeholder="Enter username" />
    <button @click="searchUserAnswers">Search</button>

    <div v-if="searchStatus === 'not-found'">
      <p>User not found.</p>
    </div>

    <div v-else-if="searchStatus === 'found-no-answers'">
      <p>User found, but no answers found.</p>
    </div>

    <div v-else-if="userAnswers.length > 0">
      <h3>User Answers</h3>
      <ul>
        <li v-for="answer in userAnswers" :key="answer.QuestionID">
          <strong>QuestionID:</strong> {{ answer.QuestionID }}
          <br>
          <strong>Radio Answer:</strong> {{ sanitize(answer.RadioAnswer) }}
          <br>
          <strong>Checkbox Answer:</strong> {{ sanitize(answer.CheckboxAnswer) }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import DOMPurify from 'dompurify';

export default {
  data() {
    return {
      searchUsername: '',
      userAnswers: [],
      searchStatus: '', // 'not-found', 'found-no-answers', or 'found-with-answers'
    };
  },
  methods: {
    searchUserAnswers() {
      fetch(`http://127.0.0.1:5000/api/user_answers?username=${this.searchUsername}`)
        .then((response) => {
          if (response.status === 404) {
            this.searchStatus = 'not-found';
            throw new Error('User not found.');
          } else if (!response.ok) {
            throw new Error('Error fetching user answers.');
          }
          return response.json();
        })
        .then((data) => {
          if (data.length === 0) {
            this.searchStatus = 'found-no-answers';
          } else {
            this.searchStatus = 'found-with-answers';
            this.userAnswers = data;
          }
        })
        .catch((error) => {
          console.error("Error fetching user answers:", error);
          this.userAnswers = [];
        });
    },
    sanitize(content) {
      return DOMPurify.sanitize(content);
    },
  },
};
</script>
