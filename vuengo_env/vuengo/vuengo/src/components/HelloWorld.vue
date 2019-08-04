<template>
  <div class="hello">
    <h1 class="title">Vuengo</h1> <!-- Page title -->

    <hr>

    <div class="columns">
      <div class="column is-one-third is-offset-one-third"> <!-- Narrow centered column -->
        <form v-on:submit.prevent="addTask"><!-- Form for adding tasks -->
          <h2 class="subtitle">Add task</h2>

          <div class="field"> <!-- Normal input field for the description -->
            <label class="label">Description</label>
            <div class="control">
              <input class="input" type="text" v-model="description">
            </div>
          </div>

          <div class="field"> <!-- Select field for choosing the status (0 and 1 as value, same as in the django status choices) -->
            <label class="label">Status</label>
            <div class="control">
              <div class="select">
                <select v-model="status">
                  <option value="0">To do</option>
                  <option value="1">Done</option>
                </select>
              </div>
            </div>
          </div>

          <div class="field is-grouped"> <!-- Submit button -->
            <div class="control">
              <button class="button is-link">Submit</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <hr>

  <div class="columns">
    <div class="column is-half">
      <h2 class="subtitle">Todo</h2>

      <div class="todo">
        <div class="card" v-for="task in tasks" v-if="task.status == 0"> <!-- Loop through the tasks array, if status is 0 (to do) then we'll show it. -->
          <div class="card-content">
            <div class="content">
              <div v-if="!task.editing" @dblclick="editTask(task.id)">
                {{ task.description }} <!-- Print the task's description here -->
              </div>
              <input v-else v-model="task.description" @blur="doneEdit(task.id)" @keyup.enter="doneEdit(task.id)" @keyup.esc="cancelEdit(task.id)" v-focus>
            </div>
          </div>
          <footer class="card-footer">
            <a class=" card-footer-item" v-on:click="removeTask(task.id)">Delete</a>  
            <a class="card-footer-item" v-on:click="setStatus(task.id)">Done</a>
          </footer>
        </div>
      </div>
    </div>

    <div class="column is-half">
      <h2 class="subtitle">Done</h2>

      <div class="done">
        <div class="card" v-for="task in tasks" v-if="task.status == 1"> <!-- Loop through the tasks array, if status is 1 (done) then we'll show it. -->
          <div class="card-content">
            <div class="content">
              <div v-if="!task.editing" @dblclick="editTask(task.id)">
                {{ task.description }} <!-- Print the task's description here -->
              </div>
              <input v-else v-model="task.description" @blur="doneEdit(task.id)" @keyup.enter="doneEdit(task.id)" @keyup.esc="cancelEdit(task.id)" v-focus>
            </div>
          </div>

          <footer class="card-footer">
            <a class=" card-footer-item" v-on:click="removeTask(task.id)">Delete</a>  
          </footer>

        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>

import axios from 'axios'

export default{
  name: 'HelloWorld',
  data(){
    return{
      tasks: [],
      description: '',
      status: 0,
      editing: false,
      beforeEditCache: '',
    }
  },

  mounted(){
    this.getTasks();
  },


  directives:{
      focus:{
          inserted: function(el){
              el.focus()
          }
      }
  },

  methods:{
    getTasks(){
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/tasks/',
        auth:{
          username: 'xxx',
          password: 'xxx'
        }
      }).then(response => this.tasks = response.data);
    },

    editTask(task_id){ 
      for (let i = 0; i < this.tasks.length; i++) {
        if (this.tasks[i].id === task_id) {
          this.tasks[i].editing = true
          break
        }
      }
    },

    doneEdit(task_id){
      //todo
      
      
      let description = '';

      for (let i = 0; i < this.tasks.length; i++) {
        if (this.tasks[i].id === task_id) {
          description = this.tasks[i].description
          this.tasks[i].beforeEditCache = description
          this.tasks[i].editing = false
          break
        }
      }

      axios({
        method:'put',
        url: 'http://127.0.0.1:8000/tasks/' + task_id + '/',
        headers: {
          'Content-Type': 'application/json'
        },
        data: {
          description: description,
          beforeEditCache: description,
          editing: false
        },
        auth: {
          username: 'xxx',
          password: 'xxx'
        }
      })


    },

    cancelEdit(task_id){
      for (let i = 0; i < this.tasks.length; i++) {
        if (this.tasks[i].id === task_id) {
          this.tasks[i].description = this.tasks[i].beforeEditCache
          this.tasks[i].editing = false
          break
        }
      }
      
    },

    addTask(){
      if(this.description){
        axios({
          method: 'post',
          url: 'http://127.0.0.1:8000/tasks/',
          data:{
            description: this.description,
            status: this.status,
            editing: false,
            beforeEditCache: this.description,
          },
          auth:{
            username: 'xxx',
            password: 'xxx'
          }
        }).then((response) => {
          let newTask = {'id': response.data.id, 'description': this.description, 'status': parseInt(this.status), 'editing': false,'beforeEditCache':this.description}
          this.tasks.push(newTask)
          this.description = ''
          this.status = 0
          this.beforeEditCache = ''
          this.editing = false
        }).catch((error) => {
          console.log(error);
        });
      }
    },
    removeTask(task_id){
      axios.delete('http://127.0.0.1:8000/tasks/' + task_id + '/',
        { 
          headers: {
            'Content-Type': 'application/json'
          },
          auth: {
            username: 'xxx',
            password: 'xxx'
          },
      })
      .then((response) => {
        this.tasks.splice(task_id,1)
        console.log('remove');
        this.getTasks();
        /* for (let i = 0; i < this.tasks.length; i++) {
          if (this.tasks[i].id === task_id) {
            this.tasks.splice(task_id,1)
            break
          }
        }  */
      });
      
    },
    setStatus(task_id) {
      let description = '';

      for (let i = 0; i < this.tasks.length; i++) {
        if (this.tasks[i].id === task_id) {
          this.tasks[i].status = 1
          description = this.tasks[i].description

          break
        }
      }

      axios({
        method:'put',
        url: 'http://127.0.0.1:8000/tasks/' + task_id + '/',
        headers: {
          'Content-Type': 'application/json'
        },
        data: {
          description: description,
          status: 1,
          editing: false,
          beforeEditCache: description,
        },
        auth: {
          username: 'xxx',
          password: 'xxx'
        }
      })
    },
  }
}

</script>

<style scoped>
.select, select { /* 100% width for the select */
  width: 100%;
}

.card { /* Adding some air under the tasks */
  margin-bottom: 25px;
}

.done { /* Make the done tasks a little bit transparent */
  opacity: 0.3;
}



</style>