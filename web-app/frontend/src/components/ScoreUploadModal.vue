<template>
  <b-modal
    ref="addScoreModal"
    id="add-score-modal"
    title="Add A New Score"
    hide-footer
  >
    <b-form @submit="onSubmit" @reset="onReset" class="w-100" v-if="!isLoading">
      <b-alert v-model="isError" variant="danger" dismissible>
        {{ errorMessage }}
      </b-alert>
      <b-spinner v-if="isLoading" label="Spinning"></b-spinner>
      <b-form-group
        id="form-title-group"
        label="Title:"
        label-for="form-title-input"
      >
        <b-form-input
          id="form-title-input"
          type="text"
          v-model="title"
          required
          placeholder="Enter title"
        >
        </b-form-input>
      </b-form-group>
      <b-form-group
        id="form-composer-group"
        label="Composer:"
        label-for="form-composer-input"
      >
        <b-form-input
          id="form-composer-input"
          type="text"
          v-model="composer"
          required
          placeholder="Enter composer"
        >
        </b-form-input>
      </b-form-group>
      <b-form-group
        id="form-file-group"
        label="File:"
        label-for="form-file-input"
      >
        <b-form-file
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
          accept=".xml, .mxl, .musicxml"
          required
        ></b-form-file>
        <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div>
      </b-form-group>
      <b-button type="submit" variant="primary"> Submit </b-button>
    </b-form>
    <b-spinner label="Spinning" variant="primary" v-else></b-spinner>
  </b-modal>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      isLoading: false,
      isError: false,
      title: '',
      composer: '',
      file: null,
      errorMessage: '',
    };
  },
  methods: {
    ...mapActions('music', ['uploadScore']),
    initForm() {
      this.isLoading = false;
      this.isError = false;
      this.title = '';
      this.composer = '';
      this.file = null;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.isLoading = true;
      this.uploadScore(this).then((response) => {
        this.$refs.addScoreModal.hide();
        this.initForm();
      }).catch((error) => {
        this.initForm();
        this.isLoading = false;
        this.isError = true;
        this.errorMessage = `Upload Failed.
         ${error.response.data}`;
      });
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addScoreModal.hide();
      this.initForm();
    },
  },
  created() {
    this.initForm();
  },
};
</script>
