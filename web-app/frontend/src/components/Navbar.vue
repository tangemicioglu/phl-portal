<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand to="/">Passive Haptic Learning Portal</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">Score Library</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              Logged in as {{ user.username }}
            </template>
            <b-dropdown-item href="#">View Profile</b-dropdown-item>
            <b-dropdown-item @click="logoutUser">Log Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import router from '@/router';

export default {
  computed: mapState('auth', ['user']),
  methods: {
    ...mapActions('auth', ['logout']),
    logoutUser() {
      router.push('/auth');
      this.logout();
    },
  },
};
</script>
