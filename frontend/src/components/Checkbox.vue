<template>
    <div id="checkbox-questions">
      <h2>Checkbox Questions</h2>
      <ul>
        <li v-for="(question, questionId) in questions" :key="questionId">
          <strong>{{ sanitize(question.question) }}</strong>
          <ul>
            <li v-for="(option, index) in question.options" :key="index">
              <input
                type="checkbox"
                :id="`question_${questionId}_option_${index}`"
                :value="option"
                v-model="selectedOptions[questionId]"
              />
              <label :for="`question_${questionId}_option_${index}`">{{ sanitize(option) }}</label>
            </li>
          </ul>
        </li>
      </ul>
      <button @click="submitAnswers">Submit Answers</button>
    </div>
</template>
  
<script>
import DOMPurify from 'dompurify';

export default {
  name: 'LP',
  data() {
    return {
      questions: {},
      selectedOptions: {},
    };
  },
  watch: {
    questions: {
      immediate: true,
      handler(newQuestions) {
        this.selectedOptions = Object.fromEntries(
          Object.keys(newQuestions).map((questionId) => [questionId, []])
        );
      },
    },
  },
  mounted() {
    this.fetchQuestions();
  },
  methods: {
    fetchQuestions() {
      fetch("http://127.0.0.1:5000/api/checkbox_questions")
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

      Object.keys(this.selectedOptions).forEach((questionID) => {
        const selectedOptions = this.selectedOptions[questionID];

        if (selectedOptions && selectedOptions.length > 0) {
          answerData[questionID] = selectedOptions;
        }
      });

      fetch("http://127.0.0.1:5000/api/submit_checkbox_answers", {
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

      this.clearSelectedOptions();
    },
    clearSelectedOptions() {
      Object.keys(this.selectedOptions).forEach((questionID) => {
        this.selectedOptions[questionID] = [];
      });
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
