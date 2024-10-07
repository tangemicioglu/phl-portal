<template>
  <div>
    <b-alert variant="danger" v-model="showLoginFailedAlert" dismissible>
      Login failed, check your username or password.
    </b-alert>

    <b-form @submit="onSubmit" @reset="onReset">
      <b-form-group
        id="username-group"
        label="Username"
        label-for="username-input"
      >
        <b-form-input
          id="username-input"
          v-model="username"
          placeholder="Username"
          autocomplete="username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="password-group"
        label="Password"
        label-for="password-input"
      >
        <b-form-input
          id="password-input"
          v-model="password"
          type="password"
          placeholder="Password"
          autocomplete="current-password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">
        Login
        <span v-bind:class="{'spinner-border': loginProcessing,
          'spinner-border-sm': loginProcessing}" role="status">
        </span>
      </b-button>
    </b-form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import router from '@/router';

export default {
  data() {
    return {
      username: '',
      password: '',
      showLoginFailedAlert: false,
      loginProcessing: false,
    };
  },
  methods: {
    ...mapActions('auth', ['login']),
    async onSubmit(event) {
      this.loginProcessing = true;
      event.preventDefault();
      const success = await this.login(this);
      this.loginProcessing = false;
      if (success) {
        router.push('/');
      } else {
        this.showLoginFailedAlert = true;
      }
    },
    onReset(event) {
      event.preventDefault();
      this.username = '';
      this.password = '';
      this.showLoginFailedAlert = false;
    },
  },
};
</script>
