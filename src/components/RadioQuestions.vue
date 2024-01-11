<!-- src/components/RadioQuestions.vue -->
<!-- <template>
    <div>
        <h1>Radio Questions</h1>
        <form @submit.prevent="submitAnswers">
            {{ selectedAnswers }}
            <div v-for="(questionData, questionID) in questions" :key="questionID">
                <label>{{ questionData.question }}</label>
                <div v-for="option in questionData.options" :key="option">
                    <input type="radio" :name="`radio_question_${questionID}`" :value="option"
                        v-model="selectedAnswers[questionID]" />
                    <label>{{ option }}</label>
                    <br />
                </div>
            </div>
            <button type="submit">Submit Answers</button>
        </form>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            selectedAnswers: {},
        };
    },
    props: {
        questions: Object,
        
    },
    methods: {
        submitAnswers() {
            const answerData = {};

            Object.keys(this.selectedAnswers).forEach((questionID) => {
                const selectedAnswer = this.selectedAnswers[questionID];

                if (selectedAnswer) {
                    answerData[questionID] = selectedAnswer;
                }
            });

            console.log("testi")

            this.$emit('submit', answerData);
            this.clearSelectedAnswers();
        },
        clearSelectedAnswers() {
            Object.keys(this.selectedAnswers).forEach((questionID) => {
                this.selectedAnswers[questionID] = null;
            });
        },
    },
};
</script>
  
<style scoped>
/* Add your component-specific styles here */
</style> -->

<template>
    <div id="radio-questions">
      <h2>Radio Questions</h2>
      <ul>
        <li v-for="(question, questionId) in questions" :key="questionId">
          <strong>{{ question.question }}</strong>
          <ul>
            <li v-for="(option, index) in question.options" :key="index">
              <input
                type="radio"
                :id="`question_${questionId}_option_${index}`"
                :name="`question_${questionId}`"
                :value="option"
                v-model="selectedOptions[questionId]"
              />
              <label :for="`question_${questionId}_option_${index}`">{{ option }}</label>
            </li>
          </ul>
        </li>
      </ul>
      <button @click="submitAnswers">Submit Answers</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        questions: {},
        selectedOptions: {},
      };
    },
    mounted() {
      this.fetchQuestions();
    },
    methods: {
      fetchQuestions() {
        fetch("http://127.0.0.1:5000/api/radio_questions")
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
          const selectedOption = this.selectedOptions[questionID];
  
          if (selectedOption !== null) {
            answerData[questionID] = selectedOption;
          }
        });
  
        // Now, you can send the answers to the backend using a fetch request
        fetch("http://127.0.0.1:5000/api/submit_radio_answers", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(answerData),
        })
          .then((response) => response.json())
          .then((data) => {
            // Handle the response from the backend if needed
            alert(data.message || data.error);
          })
          .catch((error) => {
            console.error("Error submitting answers:", error);
          });
  
        // Optionally, emit an event to notify the parent component about the submission
        this.$emit("answers-submitted", answerData);
  
        // Clear selected options after submission
        this.clearSelectedOptions();
      },
      clearSelectedOptions() {
        Object.keys(this.selectedOptions).forEach((questionID) => {
          this.selectedOptions[questionID] = null;
        });
      },
    },
  };
  </script>
  
  <style>
  /* Add your component styles here */
  </style>
  