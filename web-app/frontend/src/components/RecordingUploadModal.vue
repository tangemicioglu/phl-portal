<template>
  <b-modal
    ref="recordingUploadModal"
    id="recording-upload-modal"
    title="Upload a New Recording"
    hide-footer
  >
    <b-form @submit="onSubmit" @reset="onReset" class="w-100" v-if="!isLoading">
      <b-alert v-model="isError" variant="danger" dismissible>
        {{ this.errorMessage }}
      </b-alert>
      <b-spinner v-if="isLoading" label="Spinning"></b-spinner>
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
          accept=".midi, .MID"
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
      file: null,
      errorMessage: null,
    };
  },
  methods: {
    ...mapActions('music', ['uploadRecording']),
    initForm() {
      this.file = null;
      this.isLoading = false;
      this.isError = false;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.isLoading = true;
      this.uploadRecording(this).then((success) => {
        if (success) {
          this.$refs.recordingUploadModal.hide();
          this.initForm();
        }
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
