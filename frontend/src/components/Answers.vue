<template>
    <div class="container">
      <h1>Values for Question ID: {{ questionId }}</h1>
      <div 
        class="value-box" 
        v-for="(value, index) in values" 
        :key="index"
        @click="vote(index)"
        :class="{ selected: selectedValueIndex === index }"
      >
        {{ value }} - Votes: {{ votes[index] }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'QuestionAnswers',
    data() {
      return {
        tableName: 'short_text',  // Specify your table name here
        questionId: 4,  // Specify your Question ID here
        values: [],
        votes: [],  // Array to store votes for each value
        selectedValueIndex: null  // Index of the selected value
      };
    },
    methods: {
      fetchValues() {
        fetch(`http://127.0.0.1:5000/values?table=${this.tableName}&questionId=${this.questionId}`)
          .then(response => response.json())
          .then(data => {
            this.values = data;
            this.votes = Array(data.length).fill(0);  // Initialize votes array
          })
          .catch(error => {
            console.error('Error fetching values:', error);
          });
      },
      vote(index) {
        if (this.selectedValueIndex === index) {
          return;  // Do nothing if the same box is clicked again
        }
        if (this.selectedValueIndex !== null) {
          this.votes[this.selectedValueIndex] -= 1;  // Decrement the previous vote
        }
        this.selectedValueIndex = index;
        this.votes[index] += 1;  // Increment the vote count for the selected value
      }
    },
    created() {
      this.fetchValues();
    }
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  .value-box {
    width: 300px; /* Set a fixed width for the boxes */
    border: 1px solid #ddd;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
    cursor: pointer;
  }
  .value-box.selected {
    background-color: #d9f9d9;  /*Highlight selected box*/
    border-color: #4caf50;
  }
  </style>
  