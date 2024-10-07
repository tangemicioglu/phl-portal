<template>
  <div>
    <b-alert variant="danger" v-model="showRegisterFailedAlert" dismissible>
      Registration failed — that username already exists.
    </b-alert>
    <b-alert variant="success" v-model="showRegisterSuccessAlert" dismissible>
      Successfully registered! Return to the login page to sign in.
    </b-alert>

    <b-form @submit="onSubmit" @reset="onReset">
      <b-form-group id="email-group" label="Email" label-for="email-input">
        <b-form-input
          id="email-input"
          v-model="email"
          placeholder="Email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="username-group"
        label="Username"
        label-for="username-input"
      >
        <b-form-input
          id="username-input"
          v-model="username"
          placeholder="Username"
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
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Register</b-button>
    </b-form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
      showRegisterFailedAlert: false,
      showRegisterSuccessAlert: false,
    };
  },
  computed: {
    loggingIn() {
      return this.$store.state.auth.status.loggingIn;
    },
  },
  methods: {
    ...mapActions('auth', ['register']),
    onSubmit(event) {
      event.preventDefault();
      this.register(this).then((success) => {
        this.showRegisterSuccessAlert = success;
        this.showRegisterFailedAlert = !success;
      });
    },
    onReset(event) {
      event.preventDefault();
      this.email = '';
      this.username = '';
      this.password = '';
      this.showRegisterFailedAlert = false;
      this.showRegisterSuccessAlert = false;
    },
  },
};
</script>
