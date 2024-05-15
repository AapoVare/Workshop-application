<template>
    <div id="text-questions">
      <h2>Text Questions</h2>
      <ul>
        <li v-for="(question, questionId) in questions" :key="questionId">
          <strong>{{ sanitize(question.question) }}</strong><br>
          <textarea
            :id="`question_${questionId}`"
            v-model="textAnswers[questionId]"
            @input="updateCharacterCount(questionId)"
            placeholder="Type your answer here..."
            maxlength="240"
          ></textarea>
          <div>{{ characterCount[questionId] }}/240</div>
        </li>
      </ul>
      <button @click="submitAnswers">Submit Answers</button>
    </div>
  </template>
  
  <script>
  import DOMPurify from 'dompurify';
  
  export default {
    name: 'TextQuestions',
    data() {
      return {
        questions: {},
        textAnswers: {},
        characterCount: {},
      };
    },
    watch: {
      questions: {
        immediate: true,
        handler(newQuestions) {
          this.textAnswers = Object.fromEntries(
            Object.keys(newQuestions).map((questionId) => [questionId, ''])
          );
          this.characterCount = Object.fromEntries(
            Object.keys(newQuestions).map((questionId) => [questionId, 0])
          );
        },
      },
    },
    mounted() {
      this.fetchQuestions();
    },
    methods: {
      fetchQuestions() {
        fetch("http://127.0.0.1:5000/api/short_text_questions")
          .then((response) => response.json())
          .then((data) => {
            this.questions = data;
          })
          .catch((error) => {
            console.error("Error fetching questions:", error);
          });
      },
      submitAnswers() {
        const answerData = {};
  
        Object.keys(this.textAnswers).forEach((questionID) => {
          const answer = this.textAnswers[questionID].trim();
          if (answer) {
            answerData[questionID] = answer;
          }
        });
  
        fetch("http://127.0.0.1:5000/api/submit_short_text_answers", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(answerData),
        })
          .then((response) => response.json())
          .then((data) => {
            alert(data.message || data.error);
          })
          .catch((error) => {
            console.error("Error submitting answers:", error);
          });
  
        this.$emit("answers-submitted", answerData);
  
        this.clearTextAnswers();
      },
      clearTextAnswers() {
        Object.keys(this.textAnswers).forEach((questionID) => {
          this.textAnswers[questionID] = '';
          this.characterCount[questionID] = 0;
        });
      },
      updateCharacterCount(questionId) {
        this.characterCount[questionId] = this.textAnswers[questionId].length;
      },
      sanitize(content) {
        return DOMPurify.sanitize(content);
      },
    },
  };
  </script>
  
  <style>
  /* Add your component styles here */
  </style>
  