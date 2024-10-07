<template>
  <div>
    <h1 align="center">PHL User Portal</h1>
    <LoginForm v-if="currentForm === 'login'"/>
    <RegisterForm v-else/>
    <b-button @click.prevent="toggleForm" class="toggleButton">{{toggle}}</b-button>
  </div>
</template>

<script lang="ts">
import LoginForm from '@/components/auth/LoginForm.vue';
import RegisterForm from '@/components/auth/RegisterForm.vue';

import { Vue } from 'vue-property-decorator';

export default Vue.extend({
  data() {
    return {
      currentForm: 'login',
      toggle: 'Register a New Account',
    };
  },
  components: {
    LoginForm,
    RegisterForm,
  },
  methods: {
    toggleForm() {
      this.currentForm = this.currentForm === 'login' ? 'register' : 'login';
      this.toggle = this.currentForm === 'login' ? 'Register a New Account' : 'Back to Login';
    },
  },
});
</script>

<style scoped>
.toggleButton{
  margin-top: 10px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
